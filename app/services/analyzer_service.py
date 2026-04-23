# Core Logic
from app.clients.github_client import get_user, get_repos
from app.utils.helpers import (
    analyze_languages,
    generate_insights,
    get_top_repositories,
    analyze_activity
)

def analyze_user(username):
    user = get_user(username)
    if "error" in user:
        return {"error": user["error"]}

    repos = get_repos(username)
    if isinstance(repos, dict) and "error" in repos:
        return {"error": repos["error"]}

    languages = analyze_languages(repos)
    top_repos = get_top_repositories(repos)
    activity = analyze_activity(repos)

    insights = generate_insights(languages, repos, activity)

    return {
        "user": {
            "name": user.get("name"),
            "followers": user.get("followers"),
            "public_repos": user.get("public_repos"),
        },
        "languages": languages,
        "top_repositories": top_repos,
        "activity": activity,
        "insights": insights
    }