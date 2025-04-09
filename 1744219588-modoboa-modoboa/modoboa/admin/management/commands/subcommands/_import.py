"""Django management command to import admin objects."""

import csv
import os

import progressbar
from chardet.universaldetector import UniversalDetector

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.translation import gettext as _

from modoboa.core import models as core_models
from modoboa.core.extensions import exts_pool
from modoboa.lib.exceptions import Conflict
from .... import signals


class ImportCommand(BaseCommand):
    """Command class."""

    args = "csvfile"
    help = "Import identities from a csv file"  # NOQA:A003

    def add_arguments(self, parser):
        """Add extra arguments to command."""
        parser.add_argument(
            "--sepchar", type=str, default=";", help="Separator used in file."
        )
        parser.add_argument(
            "--continue-if-exists",
            action="store_true",
            dest="continue_if_exists",
            default=False,
            help="Continue even if an entry already exists.",
        )
        parser.add_argument(
            "--crypt-password",
            action="store_true",
            default=False,
            help="Encrypt provided passwords.",
        )
        parser.add_argument("files", type=str, nargs="+", help="CSV files to import.")

    def _import(self, filename, options, encoding="utf-8"):
        """Import domains or identities."""
        superadmin = core_models.User.objects.filter(is_superuser=True).first()
        if not os.path.isfile(filename):
            raise CommandError("File not found")

        num_lines = sum(1 for line in open(filename, encoding=encoding) if line)
        pbar = progressbar.ProgressBar(
            widgets=[progressbar.Percentage(), progressbar.Bar(), progressbar.ETA()],
            maxval=num_lines,
        ).start()
        with open(filename, encoding=encoding, newline="") as f:
            reader = csv.reader(f, delimiter=options["sepchar"])
            i = 0
            for row in reader:
                if not row:
                    continue
                fct = signals.import_object.send(
                    sender=self.__class__, objtype=row[0].strip()
                )
                fct = [func for x_, func in fct if func is not None]
                if not fct:
                    continue
                fct = fct[0]
                try:
                    fct(superadmin, row, options)
                except Conflict:
                    if options["continue_if_exists"]:
                        continue
                    raise CommandError(
                        "Object already exists at line {}: {}".format(
                            i + 1, options["sepchar"].join(row[:2])
                        )
                    ) from None
                i += 1
                pbar.update(i)

        pbar.finish()

    def handle(self, *args, **options):
        """Command entry point."""
        exts_pool.load_all()
        for filename in options["files"]:
            try:
                with transaction.atomic():
                    self._import(filename, options)
            except CommandError as exc:
                raise exc
            except UnicodeDecodeError:
                self.stdout.write(
                    self.style.NOTICE(
                        _(
                            "CSV file is not encoded in UTF-8, attempting to guess "
                            "encoding"
                        )
                    )
                )
                detector = UniversalDetector()
                with open(filename, "rb") as fp:
                    for line in fp:
                        detector.feed(line)
                        if detector.done:
                            break
                    detector.close()

                self.stdout.write(
                    self.style.NOTICE(
                        _("Reading CSV file using %(encoding)s encoding")
                        % detector.result
                    )
                )
                try:
                    with transaction.atomic():
                        self._import(
                            filename, options, encoding=detector.result["encoding"]
                        )
                except UnicodeDecodeError as exc:
                    raise CommandError(
                        _("Unable to decode CSV file using %(encoding)s " "encoding")
                        % detector.result
                    ) from exc
