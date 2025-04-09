import { derived, writable } from "svelte/store";

import { getObsidianContext } from "../../context/obsidian-context";
import type { LocalTask } from "../../task-types";

export function hoverPreview(task: LocalTask) {
  return (el: HTMLElement) => {
    const { isModPressed, showPreview } = getObsidianContext();
    let currentEvent: MouseEvent | undefined;

    const hovering = writable(false);

    function handleMouseEnter(event: MouseEvent) {
      currentEvent = event;
      hovering.set(true);
    }

    function handleMouseLeave(event: MouseEvent) {
      currentEvent = undefined;
      hovering.set(false);
    }

    el.addEventListener("mouseenter", handleMouseEnter);
    el.addEventListener("mouseleave", handleMouseLeave);

    const shouldShowPreview = derived(
      [isModPressed, hovering],
      ([$isModPressed, $hovering]) => {
        return $isModPressed && $hovering;
      },
    );

    const unsubscribe = shouldShowPreview.subscribe((newValue) => {
      if (newValue && task.location?.path && currentEvent) {
        showPreview(
          el,
          currentEvent,
          task.location.path,
          task.location.position?.start?.line,
        );
      }
    });

    return {
      destroy() {
        el.removeEventListener("mouseenter", handleMouseEnter);
        el.removeEventListener("mouseleave", handleMouseLeave);
        unsubscribe();
      },
    };
  };
}
