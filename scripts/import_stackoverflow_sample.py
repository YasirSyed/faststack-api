import os
import pandas as pd
import warnings
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer
from app.models.comment import Comment
from app.models.tag import Tag
from sqlalchemy import text
from app.core.security import get_password_hash
import numpy as np

# Suppress bcrypt warning
warnings.filterwarnings("ignore", message=".*bcrypt.*")

DATA_DIR = "data"

def clear_database(db: Session):
    # Clear association table first if it exists
    db.execute(text("DELETE FROM question_tags;"))
    db.query(Comment).delete()
    db.query(Answer).delete()
    db.query(Question).delete()
    db.query(Tag).delete()
    db.query(User).delete()
    db.commit()

# Run the script with python3 -m scriptsimport_stackoverflow_sample
def main():
    db: Session = SessionLocal()
    clear_database(db)
    print("\nDatabase cleared successfully!\n")

    # Load questions (limit to 100)
    questions_df = pd.read_csv(os.path.join(DATA_DIR, "Questions.csv"))
    questions_df = questions_df.head(100)
    question_ids = set(questions_df['Id'].astype(int))

    # Load users related to questions
    users_df = pd.read_csv(os.path.join(DATA_DIR, "Users.csv"))
    question_user_ids = set(questions_df['OwnerUserId'].dropna().astype(int))
    users_to_import = users_df[users_df['Id'].isin(list(question_user_ids))]

    # Insert all users upfront
    hashed_password = get_password_hash("password")
    for _, row in users_df.iterrows():
        display_name = row['DisplayName']
        user_id = int(row['Id'])  # Ensure integer
        # Ensure username is a string and not NaN
        if (not isinstance(display_name, (pd.Series, np.ndarray))) and (pd.isna(display_name) or str(display_name).strip() == ""):
            username = f"user{user_id}"
        else:
            username = str(display_name)
        # Ensure username is unique
        existing_user_by_username = db.query(User).filter(User.username == username).first()
        if isinstance(existing_user_by_username, User) and existing_user_by_username.id != user_id:  # type: ignore
            username = f"{username}_{user_id}"
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            user = User(
                id=user_id,
                username=username,
                email=f"user{user_id}@example.com",
                reputation=row.get('Reputation', 1),
                bio=row.get('AboutMe', None),
                hashed_password=hashed_password,
            )
            db.add(user)
            # print(f"Inserted user {user_id} with username '{username}'")
        else:
            setattr(user, "username", username)
            setattr(user, "email", f"user{user_id}@example.com")
            setattr(user, "reputation", row.get('Reputation', 1))
            setattr(user, "bio", row.get('AboutMe', None))
            setattr(user, "hashed_password", hashed_password)
            print(f"Updated user {user_id} with username '{username}'")
        db.commit()

    print("\nUsers imported successfully!\n")

    # Insert questions
    user_id_map = {user.id: user.id for user in db.query(User).all()}
    for _, row in questions_df.iterrows():
        owner_user_id = row['OwnerUserId']
        author_id = None
        if not isinstance(owner_user_id, (pd.Series, np.ndarray)):
            if not pd.isna(owner_user_id):
                author_id = int(owner_user_id)
        if not author_id or author_id not in user_id_map:
            print(f"Skipping question {row['Id']} because author {author_id} not found in imported users.")
            continue
        view_count = row['ViewCount']
        if not isinstance(view_count, (pd.Series, np.ndarray)):
            view_count_value = int(view_count) if not pd.isna(view_count) else 0
        else:
            view_count_value = 0  # or handle as needed
        question = Question(
            id=int(row['Id']),
            title=row['Title'],
            content=row['Body'],
            author_id=author_id,
            view_count=view_count_value,
            updated_at=None  # or parse if you have the date
        )
        db.merge(question)
    db.commit()

    # Get only the IDs of questions actually inserted
    inserted_question_ids = set(int(q.id) for q in db.query(Question.id).all())

    print("\nQuestions imported successfully!\n")

    # Load and insert answers related to these questions
    answers_df = pd.read_csv(os.path.join(DATA_DIR, "Answers.csv"))
    answers_to_import = answers_df[answers_df['ParentId'].isin(list(inserted_question_ids))]
    answer_user_ids = set(int(uid) for uid in answers_to_import['OwnerUserId'].dropna().astype(int))  # type: ignore

    for _, row in answers_to_import.iterrows():
        owner_user_id = row['OwnerUserId']
        author_id = None
        if not isinstance(owner_user_id, (pd.Series, np.ndarray)):
            if not pd.isna(owner_user_id):
                author_id = int(owner_user_id)
        if not author_id or author_id not in user_id_map:
            print(f"Skipping answer {row['Id']} because author {author_id} not found in imported users.")
            continue
        parent_id_value = row['ParentId']
        if not isinstance(parent_id_value, (pd.Series, np.ndarray)) and pd.isna(parent_id_value):
            print(f"Skipping answer {row['Id']} because ParentId is NaN.")
            continue
        parent_id = int(parent_id_value)
        if parent_id not in inserted_question_ids:
            print(f"Skipping answer {row['Id']} because question {parent_id} not found in imported questions.")
            continue
        answer = Answer(
            id=int(row['Id']),
            content=row['Body'],
            question_id=parent_id,
            author_id=author_id,
            is_accepted=(row['Id'] == row.get('AcceptedAnswerId', False))
        )
        db.merge(answer)
    db.commit()

    print("\nAnswers imported successfully!\n")

    # After inserting answers and committing
    inserted_answer_ids = set(int(a.id) for a in db.query(Answer.id).all())

    # Load and insert comments related to these questions/answers
    comments_df = pd.read_csv(os.path.join(DATA_DIR, "Comments.csv"))
    post_ids = list(inserted_question_ids.union(inserted_answer_ids))
    comments_to_import = comments_df[comments_df['PostId'].isin(post_ids)]
    comment_user_ids = set(int(uid) for uid in comments_to_import['UserId'].dropna().astype(int))  # type: ignore

    for _, row in comments_to_import.iterrows():
        user_id = row['UserId']
        author_id = None
        if not isinstance(user_id, (pd.Series, np.ndarray)):
            if not pd.isna(user_id):
                author_id = int(user_id)
        if author_id and author_id not in user_id_map:
            print(f"Skipping comment {row['Id']} because author {author_id} not found in imported users.")
            continue
        post_id = int(row['PostId'])
        question_id = post_id if post_id in inserted_question_ids else None
        answer_id = post_id if post_id in inserted_answer_ids else None
        if question_id is None and answer_id is None:
            print(f"Skipping comment {row['Id']} because PostId {row['PostId']} is not a valid question or answer.")
            continue
        comment = Comment(
            id=int(row['Id']),
            content=row['Text'],
            author_id=author_id if author_id else None,
            question_id=question_id,
            answer_id=answer_id,
        )
        db.merge(comment)
    db.commit()

    print("\nComments imported successfully!\n")

    # Load and insert tags related to these questions
    tags_df = pd.read_csv(os.path.join(DATA_DIR, "Tags.csv"))
    post_tags_df = pd.read_csv(os.path.join(DATA_DIR, "PostTags.csv"))
    tags_to_import = post_tags_df[post_tags_df['PostId'].isin(list(inserted_question_ids))]
    tag_ids = set(int(tid) for tid in tags_to_import['TagId'])
    tags_final = tags_df[tags_df['Id'].isin(list(tag_ids))]
    for _, row in tags_final.iterrows():
        tag = Tag(
            id=int(row['Id']),
            name=row['TagName'],
            description=None
        )
        db.merge(tag)
    db.commit()
    # Associate tags with questions
    for _, row in tags_to_import.iterrows():
        question_id = int(row['PostId'])
        tag_id = int(row['TagId'])
        question = db.query(Question).filter_by(id=question_id).first()
        tag = db.query(Tag).filter_by(id=tag_id).first()
        if question and tag:
            question.tags.append(tag)
    db.commit()

    print("\nTags imported successfully!\n")

    db.close()
    print("\nSample Stack Overflow data imported successfully!\n")

if __name__ == "__main__":
    main() 