import type { DayPlannerSettings } from "../settings";
import type { Task, WithTime } from "../task-types";

import { getMinutesSinceMidnight } from "./moment";
import { createTimestamp, getOneLineSummary } from "./task-utils";

export function notifyAboutStartedTasks(
  tasks: WithTime<Task>[],
  settings: DayPlannerSettings,
) {
  if (tasks.length === 0) {
    return;
  }

  const firstTask = tasks[0];
  const summary = getOneLineSummary(firstTask);
  const timestamp = createTimestamp(
    getMinutesSinceMidnight(firstTask.startTime),
    firstTask.durationMinutes,
    settings.timestampFormat,
  );

  new Notification(`Task started: ${summary}
${timestamp}`);
}
