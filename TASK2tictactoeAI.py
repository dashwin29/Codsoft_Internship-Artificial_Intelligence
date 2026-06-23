def pr(b):
    print("\n  0 1 2\n")
    for i in range(3):
        print(f"{i} {b[i*3]} {b[i*3+1]} {b[i*3+2]}\n")

def w(b, p):
    w_c = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    return any(all(b[i]==p for i in c) for c in w_c)

def emp(b):
    return [i for i in range(9) if b[i]==' ']

def ev(b):
    if w(b, 'X'): return 10
    if w(b, 'O'): return -10
    return 0

def mm(b, d, mx):
    if w(b,'X'): return 10
    if w(b,'O'): return -10
    if not emp(b): return 0
    
    if mx:
        s = -1000
        for i in emp(b):
            b[i]='X'
            s = max(s, mm(b, d+1, False))
            b[i]=' '
        return s
    else:
        s = 1000
        for i in emp(b):
            b[i]='O'
            s = min(s, mm(b, d+1, True))
            b[i]=' '
        return s

def ai(b):
    bm = -1000
    bv = 0
    for i in emp(b):
        b[i]='X'
        v = mm(b, 0, False)
        b[i]=' '
        if v > bm:
            bm = v
            bv = i
    return bv

def play():
    b = [' ']*9
    print("\n🎮 TIC-TAC-TOE AI (Minimax)\n")
    print("You: O | AI: X\n")
    
    while True:
        pr(b)
        
        if w(b,'X'):
            print("AI wins!")
            break
        if w(b,'O'):
            print("You win!")
            break
        if not emp(b):
            print("Draw!")
            break
        
        try:
            m = int(input("Your move (0-8): "))
            if m not in emp(b):
                print("Invalid! Try again.")
                continue
            b[m]='O'
        except:
            print("Invalid input!")
            continue
        
        if not emp(b) and not w(b,'O'):
            ai_m = ai(b)
            b[ai_m]='X'
            print(f"AI plays: {ai_m}\n")

if __name__ == "__main__":
    play()