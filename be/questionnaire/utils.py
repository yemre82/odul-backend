def get_winners(data):
    winner = ""
    vote = 0
    for i in data:
        if (i.total_vote > vote):
            winner = i.name
            vote = i.total_vote
    
    for i in data:
        if winner == i.name:
            return i
    
    return None
    