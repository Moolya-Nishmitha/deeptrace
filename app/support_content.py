SUPPORT_CONTENT = {
    "urgent": {
        "title": "Urgent — Take These Steps Now",
        "steps": [
            {
                "heading": "1. Report it on the platform immediately",
                "text": "Under India's IT Rules 2026, platforms are legally required to act on flagged non-consensual intimate imagery within 2 hours. Use the platform's in-app \"report\" feature and select the option closest to \"non-consensual intimate content\" or \"impersonation.\""
            },
            {
                "heading": "2. Call the national cybercrime helpline: 1930",
                "text": "Available 24/7. Tell them clearly that this involves non-consensual or deepfake intimate imagery — this affects how urgently they act."
            },
            {
                "heading": "3. File a complaint at cybercrime.gov.in",
                "text": "Under \"Report Other Cyber Crime.\" You'll get a complaint reference number — save it."
            },
            {
                "heading": "4. Preserve evidence before it disappears",
                "text": "Screenshots, the URL, usernames, timestamps. Don't wait until after reporting to do this — content can be taken down or deleted by others before you've captured it."
            },
        ],
        "closing": "You are not at fault for this happening to you."
    },
    "contained": {
        "title": "Steps You Can Take",
        "steps": [
            {
                "heading": "1. Preserve evidence first",
                "text": "Screenshot everything — the image, where you found it, any accompanying text, usernames, dates. Use the \"Generate Evidence Summary\" below to create a record with file hashes, which helps establish the image hasn't been tampered with after the fact."
            },
            {
                "heading": "2. File a complaint at cybercrime.gov.in",
                "text": "Under \"Report Other Cyber Crime.\" This creates an official record even if you're not pursuing it urgently right now."
            },
            {
                "heading": "3. Report it on the platform too, if applicable",
                "text": "Platforms are now required under the IT Rules 2026 amendment to label or remove flagged synthetic content within set timeframes."
            },
            {
                "heading": "4. Consider whether people around you need to know",
                "text": "If this could affect your workplace, family, or community, deciding who to tell (and when) is entirely your call, not something you owe anyone an explanation for."
            },
        ],
        "closing": None
    },
    "known_perpetrator_addendum": {
        "heading": "If you know who did this",
        "text": "Knowing who created or shared this matters — it strengthens a police complaint (FIR) and can support legal action under India's Bharatiya Nyaya Sanhita provisions for cognizable offenses. Keep any evidence of their identity (messages, account handles, prior interactions) alongside your other evidence. A local cyber cell or police station can advise on next steps once you have a complaint reference number from cybercrime.gov.in."
    }
}


def get_support_path(is_intimate: bool, is_spreading: bool) -> str:
    """Decides which guidance path applies based on the two key questions."""
    if is_intimate and is_spreading:
        return "urgent"
    return "contained"