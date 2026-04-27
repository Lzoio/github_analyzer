# Small reusable functions (Logic)
from datetime import datetime, timezone
from collections import Counter


def analyze_languages(repos):
    languages = {}

    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
        
    return languages

def get_top_repositories(repos, top_number=5):
    # Sort repos by stars
    sorted_repos = sorted(
        repos,
        key=lambda r: r.get("stargazers_count", 0),
        reverse=True 
    )

    top_repos = []

    for repo in sorted_repos[:top_number]:
        top_repos.append({
            "name": repo.get("name"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language"),
            "url": repo.get("html_url")
        })
    
    return top_repos

def analyze_activity(repos):
    if not repos:
        return {"activity_score": 0, "message": "No recent activity"}

    recent_updates = 0
    now = datetime.now(timezone.utc)

    for repo in repos:
        updated_at = repo.get("updated_at")
        if updated_at:
            last_update = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
            days_diff = (datetime.now() - last_update.replace(tzinfo=None)).days

            if days_diff < 30:
                recent_updates += 1
    
    activity_score = recent_updates / len(repos)

    return {
        "recent_active_repos": recent_updates,
        "activity_score": round(activity_score, 2)
    }

def analyze_contributions(events):
    if not events:
        return {"message": "No recent activity"}
    
    event_types = Counter()
    monthly_activity = Counter()
    repo_activity = Counter()

    now = datetime.now(timezone.utc)

    for event in events:
        event_type = event.get("type")
        repo_name = event.get("repo", {}).get("name")

        created_at = event.get("created_at")
        if created_at:
            date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            month_key = date.strftime("%Y-%m")

            monthly_activity[month_key] += 1
        
        if event_type:
            event_types[event_type] += 1
        
        if repo_name:
            repo_activity[repo_name] += 1
    
    top_repo = repo_activity.most_common(1)
    top_repo = top_repo[0] if top_repo else None

    return {
        "total_events": len(events),
        "event_types": dict(event_types),
        "monthly_activity": dict(monthly_activity),
        "most_active_repo": top_repo
    }


def generate_insights(languages, repos, activity, contributions):
    insights = []

    if not repos:
        return ["No public repositories found."]
    
    repo_count = len(repos)

    # Language dominance
    if languages:
        top_lang = max(languages, key=languages.get)
        dominance = languages[top_lang] / sum(languages.values())

        if dominance > 0.6:
            insights.append(f"Strong specialization in {top_lang}")
        else:
            insights.append("Diverse tech stack")
    
    print(f"[DEBUG] Repo count for user classification: {len(repos)}")
    
    # Project volume
    if repo_count > 50:
        insights.append("Experienced Developer (+50 projects)")
    elif repo_count > 20:
        insights.append("Active Developer (20 - 50 projects)")
    else:
        insights.append("Growing Developer (<20 projects)")
    
    # Activity Insights
    if activity["activity_score"] > 0.5:
        insights.append("Highly active recently")
    elif activity["activity_score"] > 0.2:
        insights.append("Moderately active")
    else: 
        insights.append("Low recent activity")
    
    # Contributions insights
    event_types =  contributions.get("event_types", {})

    if event_types.get("PushEvent", 0) > 50:
        insights.append("High-frequency contributor with a focus on code iteration.")
    elif event_types.get("PushEvent", 0) > 20:
        insights.append("Steady contributor with consistent development activity.")
    else:
        insights.append("Building momentum in code contributions.")

    if event_types.get("PullRequestEvent", 0) > 10:
        insights.append("Strong collaborator; experienced with peer reviews and teamwork.")
    else:
        insights.append("Primarily focuses on independent repository management.")

    if len(contributions.get("monthly_activity", {})) > 3:
        insights.append("Demonstrates long-term commitment and development consistency.")

    return insights
