from difflib import SequenceMatcher
from datetime import datetime, timedelta
from backend.models import Item, Notification, db

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_potential_matches(lost_item, found_items, threshold=0.3):
    matches = []
    
    print(f"Looking for matches for lost item: {lost_item.title}")
    print(f"Lost item description: {lost_item.description}")
    
    # First check for exact matches
    for found_item in found_items:
        if found_item.matched_with is not None:
            continue
            
        print(f"\nComparing with found item: {found_item.title}")
        print(f"Found item description: {found_item.description}")
        
        # Check for exact match (case insensitive)
        if (lost_item.title.lower() == found_item.title.lower() and 
            lost_item.description.lower() == found_item.description.lower()):
            print("Found exact match!")
            matches.append({
                'found_item': found_item,
                'score': 1.0,
                'is_exact_match': True
            })
            # Return immediately for exact match
            return matches
    
    # If no exact match found, proceed with similarity matching
    lost_words = set((lost_item.title + " " + lost_item.description).lower().split())
    
    for found_item in found_items:
        if found_item.matched_with is not None:
            continue
            
        # Skip if we already checked this item for exact match
        if any(m['found_item'].id == found_item.id for m in matches):
            continue
            
        found_words = set((found_item.title + " " + found_item.description).lower().split())
        
        # Calculate word overlap
        word_overlap = len(lost_words.intersection(found_words)) / len(lost_words.union(found_words))
        print(f"Word overlap score: {word_overlap}")
        
        # Calculate title similarity
        title_similarity = similar(lost_item.title, found_item.title)
        print(f"Title similarity score: {title_similarity}")
        
        # Calculate description similarity
        desc_similarity = similar(lost_item.description, found_item.description)
        print(f"Description similarity score: {desc_similarity}")
        
        # Calculate overall match score
        match_score = (word_overlap + title_similarity + desc_similarity) / 3
        print(f"Overall match score: {match_score}")
        
        if match_score >= threshold:
            print(f"Match found! Score: {match_score}")
            matches.append({
                'found_item': found_item,
                'score': match_score,
                'is_exact_match': False
            })
    
    # Sort matches by score
    matches.sort(key=lambda x: x['score'], reverse=True)
    print(f"\nTotal matches found: {len(matches)}")
    return matches

def create_notification(db, user, item, matched_items):
    # Check if it's an exact match
    if matched_items and matched_items[0].get('is_exact_match', False):
        message = f"Found an exact match for your {item.title}! Check the Matched Items section."
    # Create notification message for similarity matches
    elif len(matched_items) == 1:
        message = f"Your {item.title} matches with a found item! Check the Matched Items section."
    else:
        message = f"Your {item.title} matches with {len(matched_items)} found items! Check the Matched Items section."
    
    # Create notification
    notification = Notification(
        user_id=user.id,
        item_id=item.id,
        message=message,
        is_read=False
    )
    
    db.session.add(notification)
    db.session.commit()

def process_matches(db, lost_item):
    from backend.models import Item
    
    print("\nProcessing matches for lost item:", lost_item.title)
    
    # Get all unmatched found items
    found_items = Item.query.filter_by(
        status='found', 
        matched_with=None
    ).all()
    
    print(f"Found {len(found_items)} potential items to match against")
    
    # Find potential matches
    matches = find_potential_matches(lost_item, found_items)
    
    if matches:
        print("\nFound matches! Processing best match...")
        # Get the best match (highest score)
        best_match = matches[0]
        found_item = best_match['found_item']
        
        print(f"Best match: {found_item.title} with score {best_match['score']}")
        
        # Link the items together
        lost_item.matched_with = found_item.id
        found_item.matched_with = lost_item.id
        
        print(f"Linking items: Lost item {lost_item.id} with Found item {found_item.id}")
        
        # Create notification for the user
        create_notification(db, lost_item.owner, lost_item, matches)
        
        # Save changes to database
        db.session.commit()
        print("Changes saved to database")
        
        # Return the matches
        return matches
    
    print("No matches found")
    return [] 