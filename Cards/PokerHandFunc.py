def poker_hand(hand):
    suits = []
    ranks = []
    for cards in hand:
        if len(cards) not in (2,3):
            raise ValueError("All cards must be valid")
        if len(cards)==3:
            ranks.append(10)
            
        else:            
         if cards[0]=='A':
             ranks.append(14)
         elif cards[0]=='K':
             ranks.append(13)    
         elif cards[0]=='Q':
             ranks.append(12)    
         elif cards[0]=='J':
             ranks.append(11)
         else:
             ranks.append(int(cards[0]))    
               
        suits.append(cards[-1])
    sortedranks = sorted(ranks)
    possibleranks =[]
    #print(sortedranks)
    if suits.count(suits[0])==5:
        if 14 in sortedranks and 13 in sortedranks and 12 in sortedranks \
        and 11 in sortedranks and 10 in sortedranks:
         possibleranks.append(10)
        elif all(sortedranks[i]==(sortedranks[i-1]+1) for i in range(1,len(sortedranks))):
         possibleranks.append(9)    
        else:
            possibleranks.append(6)
    if all(sortedranks[i]==(sortedranks[i-1]+1) for i in range(1,len(sortedranks))):
        possibleranks.append(5)
    UniqueCards = list(set(ranks))
    if len(UniqueCards)==2:
           
        counts = [sortedranks.count(val) for val in UniqueCards]
        if 4 in counts:
            possibleranks.append(8)  # Four of a Kind
        elif sorted(counts) == [2, 3]:
            possibleranks.append(7)  # Full House
    elif len(UniqueCards)==3:
       for val in UniqueCards:
          if sortedranks.count(val)==3:
             possibleranks.append(4)
          elif sortedranks.count(val)==2:
             possibleranks.append(3)   
    elif len(UniqueCards)==4:
       possibleranks.append(2)
       
    if not possibleranks:
        possibleranks.append(1)
    
    PokerHandRanks = {10:"Royal Flush",9:"Straight Flush",8:"Four of a Kind",7:"Full House",
                      6:"Flush",5:"Straight",4:"Three of a kind",
                      3:"Two Pair",2:"Pair",1:"High Card"}
    
    output = PokerHandRanks[max(possibleranks)]
    print(hand,output)
   # print(possibleranks)
    return output    
   

if __name__ == "__main__":
    #royal flush
    poker_hand(['AH','KH','QH','JH','10H'])
    #straight flush
    poker_hand(['QH','JH','10H','9H','8H'])
    #flush when only suits are matching not in order
    poker_hand(['8H','2H','AH','5H','9H'])
    #ok so in four of a kind we don't care about the fifth unmatched card
    poker_hand(['5S','5H','5C','5D','10H'])    
    # Full House (three of a kind + a pair)
    poker_hand(['6S','6H','6D','9C','9H'])    
    # Flush (all same suit, not in sequence)
    poker_hand(['8H','2H','4H','5H','9H'])    
    # Straight (consecutive ranks, mixed suits)
    poker_hand(['9C','8H','7S','6D','5H'])    
    # Three of a Kind (three cards same rank)
    poker_hand(['4S','4H','4C','9D','2H'])    
    # Two Pair (two different pairs + one kicker)
    poker_hand(['8S','8D','3H','3C','6H'])    
    # One Pair (one pair + three unmatched)
    poker_hand(['9S','9H','5D','3C','2H'])    
    # High Card (no combination)
    poker_hand(['AS','10D','7H','4C','2S'])


