
# Virtual Assistant

## Personalised News Feed
   1. Latest news based on user's interest (taken as input during signup process) is displayed on the dashboard.

## Reminder
   1. Reminders can be added and marked as complete by the user manually. Alert is not implemented.

## Gmail
   1. Reminders are added based on the unread emails of the user.
   2. Emails (from Gmail) of a single user is fetched everytime because authentication is required to access Gmail which is beyond our scope.

## Voice
   1. The round button on dashboard is needed to be clicked to enable voice input.
   2. In dashboard, we can perform the below commands using voice:
      a. Add note - "121", "title", "text"
      b. Add reminder - "131", "title", "date", "time"
      c. Web Search - "SEARCH" must be present in the command to enable web search
      d. Current time - "CURRENT TIME" must be present in the command
      e. Name of Virtual Assistant - "YOUR NAME" must be present in the command
      Note: Codes like "121" and "131" is used to avoid the issue of noise while speaking.
   3. Reminder and Note pages also have the round button which can be clicked to add reminder and note respectively using voice.

