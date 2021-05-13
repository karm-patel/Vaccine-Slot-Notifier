from app import db, Feedback

feedbacks = Feedback().query.all()
for ind,feedback in enumerate(feedbacks):
    print(f"{ind+1}:{feedback.name}")
    print(feedback.feedback)
    print()
