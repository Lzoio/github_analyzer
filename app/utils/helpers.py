# Small reusable functions (Logic)
from datetime import datetime, timezone


def analyze_languages(repos):
    languages = {}

    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
        
    return languages

def generate_insights(languages, repos, activity):
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

    return insights

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
            days_diff = (now - last_update).days

            if days_diff < 30:
                recent_updates += 1
    
    activity_score = recent_updates / len(repos)

    return {
        "recent_active_repos": recent_updates,
        "activity_score": round(activity_score, 2)
    }
