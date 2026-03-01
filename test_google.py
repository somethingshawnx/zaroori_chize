from tools.google_tools import GmailReadTool, CalendarReadTool

def test_google_tools():
    print("Testing Google Calendar Read Tool...\n")
    calendar_tool = CalendarReadTool()
    events = calendar_tool._run()
    print("Upcoming Events:")
    print(events)
    print("\n------------------\n")
    
    print("Testing Gmail Read Tool...\n")
    gmail_tool = GmailReadTool()
    emails = gmail_tool._run()
    print("Unread Emails:")
    print(emails)

if __name__ == "__main__":
    test_google_tools()
