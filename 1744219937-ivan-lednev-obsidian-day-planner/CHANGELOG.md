## 0.27.0

### ✨ New features

- Edit text in the command palette before task creation
- Add descriptive icons to clock commands, so that they are easier to use in the mobile toolbar

## 0.26.3

### 🐞 Fixed issues

- Fix tasks not added to daily note when there is no planner heading inside it
- Fix clocks from daily notes not showing up in timeline & active clocks

## 0.26.2

### 🐞 Fixed issues

- Fix messing up frontmatter when there is no planner heading in file

## 0.26.0

### ✨ New feature: time tracking (experimental)

You can record time spent on tasks in the form of Dataview properties and then view the records as time blocks, much like planner entries. See [the docs for detailed instructions](https://github.com/ivan-lednev/obsidian-day-planner?tab=readme-ov-file#4-time-tracking).

### 🐞 Fixed issues

- Fixed crash for iOS on drag-and-drop edits (#519)
- Fixed duplicated timestamps on drag-and-drop edits (#618)
- Fixed removing task Dataview properties on edits (#370)

## 0.25.0

### 💥 Breaking changes

- Now only the items under the planner heading will get pulled from daily notes (#382)

### ✨ New features

- Now after edits there is an **UNDO** notice that lets you revert the changes to tasks, even across multiple files (partially addresses #341)
- Now the plugin will ask for permission before creating new files on drag-and-drop edits
- Tasks crossing midnight now get shown properly in multiple day columns instead of stretching the first day (#586, #364)
  - E.g.: `- 23:00 - 4:00 Task` will get shown in 2 columns as 2 separate blocks
- Timeline controls look tidier now
- Now all-day remote events are shown in the unscheduled tasks section
- Text in blocks is now sticky and will stay visible when scrolling as well as when an event starts before the configured start hour

#### Week planner -> multi-day planner

- Now you can switch between 3 views:
  - **full week** (with configurable start of the week)
  - **work week** (starting on Monday)
  - **3 upcoming days** (#515)
- You can now configure the first day of the week (#231)
- Now you can move back and forth between time periods from the sidebar of the multiday-view (#458, #495)
- Now weekends get marked by a different background color
- Now you an open plugin settings from the multi-day view
- Now the time period of the open view is visible in its tab title
- Now you can open the multi-day view from the left ribbon

### 🐞 Fixed issues

- Now the plugin finds contrasting font colors for your color overrides for time blocks (#481)
- obsidian-tasks tasks now get copied under the original line in the original file
- Now copying a task also copies the sub-items under it
- Extra spaces no longer get added in edited files

## 0.24.0

### ✨ New features

- Active task end time is now shown in status bar
- Notifications now show timestamps

### 🐞 Fixed issues

- Now tasks with no text content are not shown in timeline
- Fixed deleted recurrences of events in remote calendars showing up
- Fixed 12 am parsed as noon

## 0.23.0

### ✨ New features

- Now clicking on checkboxes on the timeline completes a task. [obsidian-tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) logic is also respected: recurrent tasks get updated, 'finished' property gets added
- There is now an option to sort items by time in your planner after an edit (thanks, @Gelio)
- You can now configure what kind of task to create on edit: bullet (`- task`) or checkbox (`- [ ] task`)
- Minimal task duration is now configurable. Now tasks won't shrink beyond this point when editing
- Timestamps get parsed anywhere on the line, not only at the start, e.g.: `- [ ] #task 20:30 - 21:00 Wake up`
  - Note that if a timestamp is not at the start of the line, it needs to be in a stricter format to avoid confusing the plugin
    - `20:00` will work
    - `2000` will not work
- There is now an option to specify your email in remote calendar config. If you do this, your RSVP status (declined/tentative) will get displayed on remote tasks from this calendar (thanks, @ramandv)

### 🐞 Fixed issues

- Now timeline will stay where you've left it when you reload Obsidian (thanks, @k4a-l)

## 0.22.0

### ✨ New features

- Default task status on creation is now configurable

### 🐞 Fixed issues

- Fixed load failure when unable to read daily notes
- Fixed console error on plugin load
- Fixed moving tasks to non-existent daily notes
- Fixed active day in week not changing on next day
- No more note switching when navigating between days from timeline view

## 0.21.1

### ✨ New features

- Drag-and-drop edits are now working on mobile: long-press on a task block to see the controls, tap on the control and start dragging to change task time
- Added floating edit controls on top of task blocks. All the edit modes are now easily available
- Now you can change task start time
- There is now a new edit mode: move block and shrink neighboring blocks
- Now you can manually adjust the height of the unscheduled tasks section through drag-and-drop

### 🐞 Fixed issues

- Fixed empty remote event names breaking the plugin (#430)
- Fixed advanced editing with Ctrl/Shift not working (#462). To do advanced edits, simply hover over the block, then over the edit controls

## 0.20.1 - 0.20.4

- 🐞 add toggle to disable release notes (#399)
- 🐞 do not reset timeline position when it's already open (#289)
- 🐞 do not replace tab content when opening weekly view (#313)
- 🐞 fix status bar error breaking plugin
- 🐞 Move task on copy, instead of changing its size
- 🐞 Fix different hourglass emoji breaking task movement
- 🐞 Fix calendar events without a location crashes plugin (#438, thanks, @sepatel)
- 🐞 Do not print undefined inside checkbox when list item is not a task (#368, thanks, @Gelio)
- 🐞 AM/PM doesn't match unexpectedly anymore (#312, thanks, @teisermann)

## 0.20.0

### New features

- ✨ Color coding: you can define background color for blocks containing certain text in first line
- ✨ Weekly view now displays unscheduled tasks on top
- ✨ Advanced drag-and-drop editing does not require modifier keys any more, you pick current edit mode in timeline controls

### Fixed issues

- 🐞 Fixed scheduling tasks for other days than today (by @Lunkle)
- 🐞 Pointer to current time is now more visible
- 🐞 Task summary in internet calendars is now displayed next to calendar name, to make it visible in short blocks

## 0.19.1 - 0.19.6

- 🐞 Fix iOS crash
- 🐞 Fix performance on startup
- 🐞 Fix colorful timeline both for local & remote calendars
- 🐞 Fix planner not reacting to daily note creation
- 🐞 Fix displaying hover preview

## 0.19.0

### ✨ New Feature: Internet Calendar Sync (Google, Outlook, iCloud)

- This lets you display events from calendars like Google Calendar, iCloud Calendar, Outlook Calendar
- You only need to add a link in the plugin settings to start displaying events from that calendar

See [README](https://github.com/ivan-lednev/obsidian-day-planner?tab=readme-ov-file#showing-internet-calendars) for details.

## 0.18.0

### ✨ New features

- Now hovering over a task with `Control` pressed will trigger a preview pop-up. This works great with the awesome [Hover Editor plugin](https://github.com/nothingislost/obsidian-hover-editor)
- Now when you click on a task, if there is an open tab for that file, the plugin is going to reuse it

## 0.17.2

### 🐞 Fixed issues

- Fix creating tasks with drag-and-drop

## 0.17.0

### 💥 Breaking changes

- Now by default, if your Dataview souce filter is empty, tasks are pulled only from visible daily notes
  - Most people never touch this field, so the plugin is going to be lightning-fast by default
  - If you want to add other folders or tags as task sources, you can still do so by adding them explicitly

### ✨ New features

- When dragging tasks from daily notes across days in the weekly view, they now get moved across files
- There is now an option to hide completed tasks from timeline
- There is now an option to hide subtasks from task blocks in the timeline

### 🐞 Fixed issues

- New drag-and-drop operations can now be started immediately after previous ones
- The plugin is much faster in the default use case (daily notes only)
- You can use plain list items in daily notes again
- Notifications work again
- Unscheduled tasks now fit their contents

### Acknowledgements

- Big thanks to @weph for helping me figure out a good performance solution
