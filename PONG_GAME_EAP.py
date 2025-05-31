import pygame, sys, random, os  # Εισάγονται οι βιβλιοθήκες: pygame για το παιχνίδι, sys για έξοδο από το πρόγραμμα, random για τυχαίες επιλογές


# Λίστα με χιουμοριστικά μηνύματα που εμφανίζονται κατά την αντίστροφη μέτρηση έναρξης
waiting_messages = [
    "Hold on tight, the game is about to get real!",  # Τυχαίο μήνυμα για ψυχαγωγία πριν ξεκινήσει το παιχνίδι
    "Are you sure you're ready for this? It's going to get intense!",
    "Game starting in 5 seconds... Try not to panic!",
    "5 seconds left... Better stretch those fingers!",
    "Get ready to fail spectacularly in 5 seconds!",
    "Time to show the world how NOT to play!",
    "5 seconds until your worst enemy (me) appears!",
    "The countdown begins... No pressure, right?",
    "Prepare yourself... or don’t, it’s up to you.",
    "Hope you're not too attached to winning!"
]

def resource_path(relative_path):
    # Προσπαθούμε να βρούμε τη "βάση" του project μας — δηλαδή από πού θα φορτωθούν τα αρχεία

    try:
        # Όταν το πρόγραμμα τρέχει ως .exe (μέσω PyInstaller), δημιουργείται ένας προσωρινός φάκελος
        # Η μεταβλητή sys._MEIPASS δείχνει εκείνον τον προσωρινό φάκελο
        base_path = sys._MEIPASS
    except Exception:
        # Όταν τρέχουμε το πρόγραμμα από το .py αρχείο (π.χ. μέσα από VS Code), το __file__ δείχνει τη διαδρομή του αρχείου
        # Παίρνουμε τον φάκελο όπου βρίσκεται το .py αρχείο
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Επιστρέφουμε το πλήρες path του αρχείου, συνδυάζοντας τη βάση (base_path) με το σχετικό path που του δίνουμε
    return os.path.join(base_path, relative_path)

# Συνάρτηση που επανατοποθετεί την μπάλα στο κέντρο και της δίνει νέα τυχαία κατεύθυνση
def reset_ball(ball, screen_width, screen_height):
    ball.x = screen_width / 2 - ball.width / 2  # Τοποθετεί την μπάλα στο κέντρο οριζόντια
    ball.y = screen_height / 2 - ball.height / 2  # Τοποθετεί την μπάλα στο κέντρο κάθετα
    ball_speed_x = 6 * random.choice((-1, 1))  # Ορίζει ταχύτητα X με τυχαία κατεύθυνση (αριστερά ή δεξιά)
    ball_speed_y = 6 * random.choice((-1, 1))  # Ορίζει ταχύτητα Y με τυχαία κατεύθυνση (πάνω ή κάτω)
    return ball_speed_x, ball_speed_y  # Επιστρέφει τις νέες ταχύτητες

# Συνάρτηση που επανατοποθετεί τις ρακέτες στο κέντρο του γηπέδου
def reset_paddles(player, cpu, player2, screen_height):
    player.centery = screen_height / 2  # Κεντράρει τον παίκτη στον άξονα Y
    cpu.centery = screen_height / 2     # Κεντράρει τη ρακέτα της CPU
    if player2:                         # Αν υπάρχει δεύτερος παίκτης (σε 2-player mode)
        player2.centery = screen_height / 2  # Κεντράρεται και αυτός στον άξονα Y

# Συνάρτηση που εμφανίζει το μήνυμα WELCOME και την αντίστροφη μέτρηση πριν ξεκινήσει το παιχνίδι
def show_starting_message(screen, screen_width, screen_height, count_sound):
    start_font = pygame.font.Font(resource_path('fonts/Nintendo-DS-BIOS.ttf'), 50)  # Ρύθμιση γραμματοσειράς για τα μηνύματα
    message = "WELCOME"  # Κύριο μήνυμα τίτλου
    text_surface = start_font.render(message, True, (255, 200, 0))  # Δημιουργεί το surface του κειμένου
    text_x = (screen_width / 2) - (text_surface.get_width() / 2)  # Κεντράρει οριζόντια
    text_y = (screen_height / 2) - (text_surface.get_height() / 2) - 50  # Κεντράρει λίγο πάνω από τη μέση
    screen.fill('gray20')  # Καθαρίζει την οθόνη με γκρι φόντο
    screen.blit(text_surface, (text_x, text_y))  # Εμφανίζει το μήνυμα
    count_sound.play(2)  # Παίζει τον ήχο αντίστροφης μέτρησης (2 φορές)

    # Επιλογή και εμφάνιση τυχαίου χιουμοριστικού μηνύματος κάτω από το WELCOME
    random_message = random.choice(waiting_messages)  # Επιλέγεται τυχαία από τη λίστα
    random_message_surface = start_font.render(random_message, True, (255, 200, 0))  # Δημιουργείται το surface
    message_x = (screen_width / 2) - (random_message_surface.get_width() / 2)  # Κέντρο οριζόντια
    message_y = text_y + text_surface.get_height() + 20  # Τοποθέτηση λίγο κάτω από το WELCOME
    screen.blit(random_message_surface, (message_x, message_y))  # Εμφανίζεται το μήνυμα στην οθόνη

    # Αντίστροφη μέτρηση από 5 έως 1
    countdown_font = pygame.font.Font(resource_path('fonts/Nintendo-DS-BIOS.ttf'), 60)  # Γραμματοσειρά για countdown
    for i in range(5, 0, -1):  # Βρόχος από 5 μέχρι 1
        # Καθαρίζει το προηγούμενο νούμερο αντίστροφης μέτρησης
        pygame.draw.rect(screen, ('gray20'), (0, message_y + random_message_surface.get_height(), screen_width, 60))
        countdown_surface = countdown_font.render(str(i), True, (255, 200, 0))  # Δημιουργεί νέο νούμερο
        countdown_x = (screen_width / 2) - (countdown_surface.get_width() / 2)  # Κέντρο οριζόντια
        countdown_y = message_y + random_message_surface.get_height() + 20     # Τοποθέτηση λίγο πιο κάτω
        screen.blit(countdown_surface, (countdown_x, countdown_y))  # Εμφανίζεται το νούμερο
        pygame.display.update()  # Ενημερώνεται η οθόνη για να το δούμε
        pygame.time.delay(1000)  # Αναμονή 1 δευτερόλεπτο

    pygame.time.delay(500)  # Τελική μικρή αναμονή πριν ξεκινήσει το παιχνίδι

# Συνάρτηση που επαναφέρει το παιχνίδι μετά από πόντο (ή στην αρχή)
def reset_game(ball, player, cpu, player2, screen_width, screen_height):
    ball_speed_x, ball_speed_y = reset_ball(ball, screen_width, screen_height)  # Επαναφορά μπάλας και ταχύτητας
    player.midright = (screen_width, screen_height / 2)  # Θέτει τον παίκτη στη δεξιά πλευρά στο κέντρο
    cpu.midleft = (0, screen_height / 2)                 # Θέτει τον CPU στην αριστερή πλευρά στο κέντρο
    if player2:                                          # Αν υπάρχει δεύτερος παίκτης
        player2.midleft = (0, screen_height / 2)         # Τοποθετείται και αυτός στην αριστερή πλευρά στο κέντρο
    return ball_speed_x, ball_speed_y  # Επιστρέφονται οι νέες ταχύτητες για τη συνέχεια



def draw_victory_message(screen, screen_width, screen_height, winner):  # Εμφανίζει μήνυμα νίκης όταν κάποιος φτάσει τους 9 πόντους
    victory_font = pygame.font.Font(resource_path('fonts/Nintendo-DS-BIOS.ttf'), 200)  # Φόρτωση μεγάλης γραμματοσειράς για το μήνυμα
    text = f"{winner} WINS!"  # Δημιουργεί το κείμενο ανάλογα με τον νικητή

    main_color = (255, 255, 0)  # Χρώμα κειμένου (κίτρινο)
    shadow_color = (30, 0, 0)   # Χρώμα σκιάς (σκούρο κόκκινο/μαύρο)

    # Δημιουργεί επιφάνειες κειμένου: σκιά + κυρίως μήνυμα
    victory_shadow = victory_font.render(text, True, shadow_color)
    victory_surface = victory_font.render(text, True, main_color)

    # Κεντράρει το μήνυμα στο παράθυρο
    text_x = screen_width / 2 - victory_surface.get_width() / 2
    text_y = screen_height / 2 - victory_surface.get_height() / 2

    shadow_offset = 7  # Απόσταση σκιάς
    screen.blit(victory_shadow, (text_x + shadow_offset, text_y + shadow_offset))  # Σχεδιάζει τη σκιά
    screen.blit(victory_surface, (text_x, text_y))  # Σχεδιάζει το κυρίως μήνυμα

    # Δημιουργεί πλαίσιο γύρω από το μήνυμα
    frame_padding = 10
    text_rect = pygame.Rect(
        text_x - frame_padding,
        text_y - frame_padding,
        victory_surface.get_width() + 2 * frame_padding,
        victory_surface.get_height() + 2 * frame_padding
    )
    pygame.draw.rect(screen, shadow_color, text_rect, width=3, border_radius=10)  # Σχεδιάζει το πλαίσιο με στρογγυλεμένες γωνίες


def point_won(winner, enemy_points, player_points, ball, screen_width, screen_height, screen, player, cpu, player2, game_over_sound, game_mode):
    # Ενημερώνει το σκορ με βάση ποιος κέρδισε τον πόντο
    if winner == "cpu":
        enemy_points += 1
    elif winner == "player":
        player_points += 1

    # Αν κάποιος φτάσει τους 9 πόντους, λήγει ο αγώνας
    if enemy_points >= 9 or player_points >= 9:
        game_over_sound.play()
        # Αν mode είναι 1player ή cpu_vs_cpu, δείχνει Player/CPU
        if game_mode == 'cpu_vs_cpu' or game_mode == '1player':
            if enemy_points >= 9:
                draw_victory_message(screen, screen_width, screen_height, "CPU")
            else:
                draw_victory_message(screen, screen_width, screen_height, "Player")
        # Αν είναι 2 παίκτες, δείχνει Player ή Player2
        if game_mode == '2players':
            if enemy_points >= 9:
                draw_victory_message(screen, screen_width, screen_height, "Player2")
            else:
                draw_victory_message(screen, screen_width, screen_height, "Player")

        pygame.display.flip()  # Ενημερώνει την οθόνη για να φανεί το μήνυμα νίκης
        pygame.time.delay(4000)  # Περιμένει 4 δευτερόλεπτα πριν συνεχίσει
        enemy_points, player_points = 0, 0  # Επαναφέρει το σκορ
        ball_speed_x, ball_speed_y = reset_game(ball, player, cpu, player2, screen_width, screen_height)  # Επαναφορά παιχνιδιού
        game_state = "menu"  # Επιστροφή στο μενού
        return enemy_points, player_points, ball_speed_x, ball_speed_y, game_state

    # Αν δεν τελείωσε ο αγώνας, κάνει reset την μπάλα
    pygame.display.flip()
    pygame.time.delay(300)
    ball_speed_x, ball_speed_y = reset_ball(ball, screen_width, screen_height)
    player.midright = (screen_width, screen_height / 2)
    if player2:
        player2.midleft = (0, screen_height / 2)

    reset_paddles(player, cpu, player2, screen_height)  # Επαναφορά ρακετών
    return enemy_points, player_points, ball_speed_x, ball_speed_y, "game"  # Συνέχιση παιχνιδιού


def animate_ball(ball, ball_speed_x, ball_speed_y, screen_width, screen_height, player, cpu, enemy_points, player_points, player2, game_mode, screen, ball_sound, point_sound, game_over_sound):
    ball.x += ball_speed_x  # Μετακίνηση μπάλας στον άξονα Χ
    ball.y += ball_speed_y  # Μετακίνηση μπάλας στον άξονα Υ

    # Αναστροφή όταν χτυπήσει πάνω ή κάτω
    if ball.top <= 0:
        ball.top = 0
        ball_speed_y *= -1
    elif ball.bottom >= screen_height:
        ball.bottom = screen_height
        ball_speed_y *= -1

    # Αν περάσει δεξιά: πόντος για CPU
    if ball.right >= screen_width:
        enemy_points, player_points, ball_speed_x, ball_speed_y, game_state = point_won(
            "cpu", enemy_points, player_points, ball, screen_width, screen_height, screen, player, cpu, player2, game_over_sound, game_mode
        )
        point_sound.play()

    # Αν περάσει αριστερά: πόντος για Player
    if ball.left <= 0:
        enemy_points, player_points, ball_speed_x, ball_speed_y, game_state = point_won(
            "player", enemy_points, player_points, ball, screen_width, screen_height, screen, player, cpu, player2, game_over_sound, game_mode
        )
        point_sound.play()

    # Καθορισμός των ρακετών που συμμετέχουν στη σύγκρουση
    paddles = []
    if game_mode == '1player':
        paddles = [player, cpu]
    elif game_mode == '2players':
        paddles = [player, player2]
    elif game_mode == 'cpu_vs_cpu':
        paddles = [player, cpu]

    # Αντιμετώπιση προβλήματος όπου η μπάλα "κολλάει" στις άκρες της ρακέτας
    for paddle in paddles:
        if ball.colliderect(paddle):
            if abs(ball.right - paddle.left) < 10 and ball_speed_x > 0:
                ball_speed_x *= -1
                ball.right = paddle.left - 1
            elif abs(ball.left - paddle.right) < 10 and ball_speed_x < 0:
                ball_speed_x *= -1
                ball.left = paddle.right + 1
            elif abs(ball.bottom - paddle.top) < 10 and ball_speed_y > 0:
                ball_speed_y *= -1
                ball.bottom = paddle.top - 1
            elif abs(ball.top - paddle.bottom) < 10 and ball_speed_y < 0:
                ball_speed_y *= -1
                ball.top = paddle.bottom + 1
            ball_sound.play()  # Ήχος απόκρουσης

    if 'game_state' not in locals():
        game_state = "game"
    return ball_speed_x, ball_speed_y, enemy_points, player_points, game_state  # Επιστροφή ενημερωμένων τιμών


def animate_player(player, player_speed, screen_height):
    player.y += player_speed  # Ενημερώνει τη θέση της ρακέτας του παίκτη
    if player.top <= 0:
        player.top = 0  # Αποτρέπει την έξοδο πάνω από την οθόνη
    if player.bottom >= screen_height:
        player.bottom = screen_height  # Αποτρέπει την έξοδο κάτω από την οθόνη


def animate_cpu(cpu, cpu_speed, ball, screen_height):
    # Απλή AI: η ρακέτα κινείται προς το κέντρο της μπάλας
    if ball.centery < cpu.centery:
        cpu_speed = -5
    elif ball.centery > cpu.centery:
        cpu_speed = 5
    else:
        cpu_speed = 0
    cpu.y += cpu_speed
    # Περιορισμός εντός της οθόνης
    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height
    return cpu_speed  # Επιστρέφει την τρέχουσα ταχύτητα


def animate_player2(player2, player2_speed, screen_height):
    player2.y += player2_speed  # Κινεί τη ρακέτα του δεύτερου παίκτη
    if player2.top <= 0:
        player2.top = 0  # Περιορισμός στο πάνω όριο
    if player2.bottom >= screen_height:
        player2.bottom = screen_height  # Περιορισμός στο κάτω όριο


# Τροποποιήσεις για εμφάνιση τρίτης επιλογής στο μενού (Press 3)
def draw_menu(screen, screen_width, screen_height, muted, sound_on_icon, sound_off_icon, sound_icon_rect):

    screen.fill('gray40')  # Καθαρίζει την οθόνη και την γεμίζει με χρώμα 'gray40'

    title_font = pygame.font.Font(resource_path('fonts/Nintendo-DS-BIOS.ttf'), 160)  # Φορτώνει τη γραμματοσειρά για τον τίτλο
    box_width = 800  # Καθορίζει το πλάτος του πλαισίου τίτλου
    box_height = 220  # Καθορίζει το ύψος του πλαισίου τίτλου
    box_x = (screen_width / 2) - (box_width / 2)  # Υπολογίζει την οριζόντια θέση ώστε να είναι κεντραρισμένο
    box_y = (screen_height / 2) - (box_height / 2) - 150  # Τοποθετεί το πλαίσιο πιο πάνω από το κέντρο της οθόνης

    # Σχεδιάζει το σκούρο κόκκινο πλαίσιο για τον τίτλο με στρογγυλεμένες γωνίες
    pygame.draw.rect(screen, (45, 0, 0), (box_x, box_y, box_width, box_height), border_radius=20)
    # Σχεδιάζει λευκό περίγραμμα γύρω από το πλαίσιο με πάχος 3 pixel και πιο έντονη στρογγυλοποίηση
    pygame.draw.rect(screen, (255, 255, 255), (box_x - 5, box_y - 5, box_width + 10, box_height + 10), width=3, border_radius=25)

    title_shadow = title_font.render("PONG GAME", True, (0, 0, 0))  # Δημιουργεί σκιά του τίτλου σε μαύρο χρώμα
    shadow_x = (screen_width / 2) - (title_shadow.get_width() / 2) + 4  # Ελαφρώς μετατοπισμένο για shadow effect
    shadow_y = (screen_height / 2) - (title_shadow.get_height() / 2) - 146
    screen.blit(title_shadow, (shadow_x, shadow_y))  # Εμφανίζει τη σκιά του τίτλου

    title_surface = title_font.render("PONG GAME", True, (255, 255, 0))  # Κύριο κείμενο του τίτλου σε κίτρινο
    title_x = (screen_width / 2) - (title_surface.get_width() / 2)
    title_y = (screen_height / 2) - (title_surface.get_height() / 2) - 150
    screen.blit(title_surface, (title_x, title_y))  # Εμφανίζει τον τίτλο πάνω από τη σκιά

    # Ρυθμίζει τη γραμματοσειρά για τις επιλογές του μενού
    start_font = pygame.font.Font(resource_path('fonts/Nintendo-DS-BIOS.ttf'), 80)

    # Επιλογή 1 - Παίξε με υπολογιστή
    start_shadow = start_font.render("Press 1 To Fight the Cpu", True, (0, 0, 0))  # Σκιά κειμένου
    start_surface = start_font.render("Press 1 To Fight the Cpu", True, (150, 255, 0))  # Κύριο κείμενο
    start_x = 50
    start_y = screen_height - 250
    start_rect = pygame.Rect(start_x - 10, start_y - 10, start_surface.get_width() + 20, start_surface.get_height() + 20)
    pygame.draw.rect(screen, (60, 0, 0), start_rect, 0)  # Φόντο της επιλογής
    pygame.draw.rect(screen, (255, 255, 255), (start_rect.x - 5, start_rect.y - 5, start_rect.width + 10, start_rect.height + 10), width=3)
    screen.blit(start_shadow, (start_x + 4, start_y + 4))  # Προσθήκη σκιάς
    screen.blit(start_surface, (start_x, start_y))  # Προσθήκη κυρίως κειμένου

    # Επιλογή 2 - Δύο παίκτες
    start2_shadow = start_font.render("Press 2 To Challenge A Friend", True, (0, 0, 0))
    start2_surface = start_font.render("Press 2 To Challenge A Friend", True, (255, 150, 0))
    start2_x = 50
    start2_y = start_y + start_surface.get_height() + 20
    start2_rect = pygame.Rect(start2_x - 10, start2_y - 10, start2_surface.get_width() + 20, start2_surface.get_height() + 20)
    pygame.draw.rect(screen, (50, 0, 0), start2_rect, 0)
    pygame.draw.rect(screen, (255, 255, 255), (start2_rect.x - 5, start2_rect.y - 5, start2_rect.width + 10, start2_rect.height + 10), width=3)
    screen.blit(start2_shadow, (start2_x + 4, start2_y + 4))
    screen.blit(start2_surface, (start2_x, start2_y))

    # Επιλογή 3 - CPU εναντίον CPU
    start3_shadow = start_font.render("Press 3 For CPU vs CPU", True, (0, 0, 0))
    start3_surface = start_font.render("Press 3 For CPU vs CPU", True, (255, 100, 255))
    start3_x = 50
    start3_y = start2_y + start2_surface.get_height() + 20
    start3_rect = pygame.Rect(start3_x - 10, start3_y - 10, start3_surface.get_width() + 20, start3_surface.get_height() + 20)
    pygame.draw.rect(screen, (30, 0, 30), start3_rect, 0)
    pygame.draw.rect(screen, (255, 255, 255), (start3_rect.x - 5, start3_rect.y - 5, start3_rect.width + 10, start3_rect.height + 10), width=3)
    screen.blit(start3_shadow, (start3_x + 4, start3_y + 4))
    screen.blit(start3_surface, (start3_x, start3_y))

    # === Εμφάνιση εικονιδίου ήχου πάνω δεξιά ===
    if muted:
        screen.blit(sound_off_icon, (sound_icon_rect.x, sound_icon_rect.y))
    else:
        screen.blit(sound_on_icon, (sound_icon_rect.x, sound_icon_rect.y))

# Συνάρτηση που σχεδιάζει την κύρια οθόνη του παιχνιδιού (μπάλα, ρακέτες, σκορ, γραμμές)
def draw_game(screen, ball, player, cpu, player2, enemy_points, player_points, screen_width, screen_height, game_mode, muted, sound_on_icon, sound_off_icon, sound_icon_rect):
    screen.fill('gray20')  # Καθαρίζει την οθόνη με γκρι χρώμα φόντου

    pygame.draw.ellipse(screen, 'plum1', ball)  # Σχεδίαση μπάλας με χρώμα "plum1"

    # Σχεδίαση των ρακετών ανάλογα με το mode του παιχνιδιού
    if game_mode == "1player":
        pygame.draw.rect(screen, (250, 150, 0), cpu)       # Αριστερή ρακέτα (CPU)
        pygame.draw.rect(screen, (150, 250, 0), player)    # Δεξιά ρακέτα (παίκτης)
    elif game_mode == "2players":
        pygame.draw.rect(screen, (250, 150, 0), player2)   # Αριστερή ρακέτα (Player 2)
        pygame.draw.rect(screen, (150, 250, 0), player)    # Δεξιά ρακέτα (Player 1)
    elif game_mode == "cpu_vs_cpu":
        pygame.draw.rect(screen, (250, 150, 0), cpu)       # Αριστερή ρακέτα (CPU)
        pygame.draw.rect(screen, (150, 250, 0), player)    # Δεξιά ρακέτα (CPU)

    # Κεντρική κάθετη γραμμή στο γήπεδο
    pygame.draw.aaline(screen, 'light goldenrod yellow', (screen_width / 2, 0), (screen_width / 2, screen_height))

    # Διακεκομμένες γραμμές που δείχνουν τα όρια κίνησης στον άξονα X
    dash_color = 'white'
    dash_height = 10
    gap = 10

    # Περιοχή σχεδίασης των ορίων (1/8 του ύψους), κεντραρισμένη
    dash_zone_height = screen_height // 8
    dash_start_y = (screen_height - dash_zone_height) // 2

    # Όριο για την CPU (1/3 του πλάτους οθόνης)
    cpu_limit_x = screen_width // 3
    for y in range(dash_start_y, dash_start_y + dash_zone_height, dash_height + gap):
        pygame.draw.line(screen, dash_color, (cpu_limit_x, y), (cpu_limit_x, y + dash_height), 1)

    # Όριο για τον παίκτη (2/3 του πλάτους οθόνης)
    player_limit_x = 2 * screen_width // 3
    for y in range(dash_start_y, dash_start_y + dash_zone_height, dash_height + gap):
        pygame.draw.line(screen, dash_color, (player_limit_x, y), (player_limit_x, y + dash_height), 1)

    # Σχεδίαση σκορ παικτών
    score_font = pygame.font.Font(resource_path('fonts/Nintendo-DS-BIOS.ttf'), 100)  # Ορισμός γραμματοσειράς
    cpu_score_surface = score_font.render(str(enemy_points), True, (250, 150, 0))  # Σκορ CPU
    player_score_surface = score_font.render(str(player_points), True, (150, 250, 0))  # Σκορ Παίκτη
    screen.blit(cpu_score_surface, (screen_width / 4, 20))  # Τοποθέτηση σκορ CPU
    screen.blit(player_score_surface, (3 * screen_width / 4, 20))  # Τοποθέτηση σκορ Παίκτη

    if muted:
        screen.blit(sound_off_icon, (sound_icon_rect.x, sound_icon_rect.y))
    else:
        screen.blit(sound_on_icon, (sound_icon_rect.x, sound_icon_rect.y))

# Συνάρτηση πρόβλεψης θέσης Y της μπάλας με αναπήδηση στους τοίχους
def predict_ball_y(ball, speed_y, screen_height):
    predicted_y = ball.y
    simulated_speed = speed_y
    while True:
        predicted_y += simulated_speed
        if predicted_y < 0:
            predicted_y = -predicted_y
            simulated_speed *= -1
        elif predicted_y > screen_height:
            predicted_y = 2 * screen_height - predicted_y
            simulated_speed *= -1
        else:
            break
    return predicted_y

# Συνάρτηση για την οριζόντια κίνηση του παίκτη (δεξιά ρακέτα)
def animate_player_horizontal(player, speed_x, screen_width, ball):
    player.x += speed_x  # Μετακίνηση ρακέτας με βάση την ταχύτητα στον άξονα Χ

    # Όρια κίνησης για τη δεξιά ρακέτα
    left_limit = screen_width * (2 / 3)         
    right_limit = screen_width - player.width

    if player.x < left_limit:
        player.x = left_limit
    if player.x > right_limit:
        player.x = right_limit

# Συνάρτηση για εξελιγμένη κίνηση CPU (με πρόβλεψη μπάλας και περιορισμούς)
def animate_cpu_advanced(cpu, ball, ball_speed_x, ball_speed_y,
                         screen_width, screen_height, cpu_start_x,
                         allow_horizontal, is_right_cpu):
    cpu_speed_y = 5  # Ταχύτητα στον κάθετο άξονα
    cpu_speed_x = 2  # Ταχύτητα στον οριζόντιο άξονα

    # Αν η μπάλα κινείται προς την CPU ρακέτα
    if (is_right_cpu and ball_speed_x > 0) or (not is_right_cpu and ball_speed_x < 0):
        predicted_y = predict_ball_y(ball, ball_speed_y, screen_height)

        # Κίνηση στον άξονα Υ ώστε να φτάσει το ύψος της μπάλας
        if abs(cpu.centery - predicted_y) > 10:
            if cpu.centery < predicted_y:
                cpu.y += cpu_speed_y
            else:
                cpu.y -= cpu_speed_y

        # Κίνηση στον Χ μόνο αν επιτρέπεται (π.χ. μετά τους 4 πόντους)
        if allow_horizontal:
            distance_x = abs(cpu.centerx - ball.centerx)
            if distance_x > 140:  # Αν η απόσταση από τη μπάλα είναι αρκετή
                target_x = ball.x
                if is_right_cpu:
                    target_x -= cpu.width
                if cpu.x < target_x:
                    cpu.x += cpu_speed_x
                elif cpu.x > target_x:
                    cpu.x -= cpu_speed_x
            else:
                # Πολύ κοντά στη μπάλα ⇒ κάνε πίσω
                if is_right_cpu:
                    cpu.x += cpu_speed_x
                else:
                    cpu.x -= cpu_speed_x

    else:
        # Όταν η μπάλα απομακρύνεται, επέστρεψε στο κέντρο
        if cpu.centery < screen_height // 2:
            cpu.y += cpu_speed_y
        elif cpu.centery > screen_height // 2:
            cpu.y -= cpu_speed_y

        if allow_horizontal:
            if cpu.x > cpu_start_x:
                cpu.x -= cpu_speed_x
            elif cpu.x < cpu_start_x:
                cpu.x += cpu_speed_x

    # Περιορισμός κίνησης μέσα στα επιτρεπτά όρια οθόνης
    cpu.top = max(cpu.top, 0)
    cpu.bottom = min(cpu.bottom, screen_height)

    # Περιορισμός κίνησης στον άξονα Χ ανάλογα με πλευρά CPU
    if is_right_cpu:
        min_x = screen_width * (2 / 3)
        max_x = screen_width - cpu.width
    else:
        min_x = 0
        max_x = screen_width * (1 / 3) - cpu.width

    if cpu.x < min_x:
        cpu.x = min_x
    if cpu.x > max_x:
        cpu.x = max_x


def animate_player2_horizontal(player2, speed_x, screen_width, ball):  # Συνάρτηση που ελέγχει την οριζόντια κίνηση του παίκτη 2 (αριστερή ρακέτα)
    player2.x += speed_x  # Ενημέρωση της θέσης στον άξονα Χ με βάση την ταχύτητα (πληκτρο A/D)

    # Όρια για τον παίκτη 2: Δεν επιτρέπεται να ξεπεράσει το 1/3 του πλάτους της οθόνης
    left_limit = 0  # Αριστερό όριο: αρχή της οθόνης
    right_limit = screen_width * (1 / 3) - player2.width  # Δεξί όριο: 1/3 του πλάτους - πλάτος ρακέτας

    if player2.x < left_limit:  # Αν προσπαθήσει να πάει πιο αριστερά απ' όσο επιτρέπεται
        player2.x = left_limit  # Τον επαναφέρουμε στο όριο

    if player2.x > right_limit:  # Αν προσπαθήσει να ξεπεράσει το δεξί όριο
        player2.x = right_limit  # Τον επαναφέρουμε στο όριο
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~MAIN FUNCTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():  # Κύρια συνάρτηση που εκτελεί το παιχνίδι
    pygame.init()  # Αρχικοποιεί όλα τα modules της βιβλιοθήκης pygame (ήχος, γραφικά, γεγονότα κλπ)
    
    pygame.event.set_blocked(pygame.MOUSEMOTION)  # Εμποδίζει την καταγραφή της κίνησης του ποντικιού — δεν τη χρειαζόμαστε εδώ
    
    pygame.mixer.init()  # Ενεργοποιεί τη λειτουργία ήχου (mixer) για αναπαραγωγή μουσικής και ηχητικών εφέ
    
    clock = pygame.time.Clock()  # Ρολόι του παιχνιδιού για τον έλεγχο των FPS (frames per second)

    screen_width = 1000  # Θέτει το πλάτος του παραθύρου σε 1000 pixels
    screen_height = 800  # Θέτει το ύψος του παραθύρου σε 800 pixels

    # Φόρτωση εικονιδίων ήχου
    sound_on_icon = pygame.image.load(resource_path('images/sound_on.png'))
    sound_off_icon = pygame.image.load(resource_path('images/sound_off.png'))

    # Ρυθμίζουμε μέγεθος (προαιρετικά)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    icon_size = (50, 50)
    sound_on_icon = pygame.transform.scale(sound_on_icon, icon_size)
    sound_off_icon = pygame.transform.scale(sound_off_icon, icon_size)


    # Ορθογώνιο περιοχής για τον έλεγχο του κλικ
    sound_icon_rect = pygame.Rect(screen_width - 60, 10, 50, 50)

    muted = False  # Αρχική κατάσταση ήχου
    
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    # Δημιουργεί το παράθυρο του παιχνιδιού με δυνατότητα αλλαγής μεγέθους από τον χρήστη
    
    pygame.display.set_caption("PONG GAME EAP!")  # Θέτει τον τίτλο του παραθύρου του παιχνιδιού

    game_state = "menu"  # Η αρχική κατάσταση είναι το "μενού" πριν ξεκινήσει κάποιο mode παιχνιδιού
    game_mode = None  # Δεν έχει επιλεγεί ακόμα τρόπος παιχνιδιού (1player, 2players, cpu_vs_cpu)
    music_started = False  # Δείχνει αν έχει ξεκινήσει η μουσική στο παρασκήνιο
    

    # Φόρτωση ήχων και ρύθμιση έντασης
    pygame.mixer.music.load(resource_path("sound/music.wav"))  # Φόρτωση αρχείου μουσικής
    pygame.mixer.music.set_volume(0.8)  # Ρύθμιση έντασης μουσικής στο 80%

    ball_sound = pygame.mixer.Sound(resource_path('sound/ball.wav'))  # Ήχος αναπήδησης της μπάλας
    ball_sound.set_volume(1)  # Πλήρης ένταση για το bounce της μπάλας

    point_sound = pygame.mixer.Sound(resource_path('sound/point_lost.wav'))  # Ήχος όταν κάποιος χάνει πόντο
    point_sound.set_volume(0.3)  # Χαμηλότερη ένταση

    game_over_sound = pygame.mixer.Sound(resource_path('sound/game_over.wav'))  # Ήχος λήξης παιχνιδιού
    count_sound = pygame.mixer.Sound(resource_path('sound/countdown.wav'))  # Ήχος αντίστροφης μέτρησης στην αρχή
    count_sound.set_volume(0.3)

    # Δημιουργία βασικών αντικειμένων του παιχνιδιού
    ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 27, 27)
    # Δημιουργία της μπάλας ως ορθογώνιο (Rect) στο κέντρο της οθόνης

    ball.center = (screen_width / 2, screen_height / 2)  # Τοποθετεί το κέντρο της μπάλας στο κέντρο της οθόνης

    cpu = pygame.Rect(0, 0, 20, 100)  # Η αριστερή ρακέτα του υπολογιστή, ξεκινάει από πάνω αριστερά
    cpu.centery = screen_height / 2  # Την τοποθετούμε κατακόρυφα στο κέντρο

    player = pygame.Rect(0, 0, 20, 100)  # Η δεξιά ρακέτα (παίκτης 1)
    player.midright = (screen_width, screen_height / 2)  # Την τοποθετούμε δεξιά, στο κέντρο του ύψους

    player2 = pygame.Rect(0, 0, 20, 100)  # Ρακέτα για τον δεύτερο παίκτη (σε mode 2-players)
    player2.midleft = (0, screen_height / 2)  # Την τοποθετούμε αριστερά, στο κέντρο του ύψους

    # Ρύθμιση αρχικών τιμών ταχυτήτων και σκορ
    ball_speed_x, ball_speed_y = reset_ball(ball, screen_width, screen_height)
    # Θέτει αρχικές τυχαίες ταχύτητες στη μπάλα καλώντας τη reset_ball

    player_speed = 0           # Κατακόρυφη ταχύτητα για τον παίκτη
    player_speed_x = 0         # Οριζόντια ταχύτητα για τον παίκτη (μετά τους 4 πόντους)
    player2_speed = 0          # Κατακόρυφη ταχύτητα για τον παίκτη 2
    player2_speed_x = 0        # Οριζόντια ταχύτητα για τον παίκτη 2 (μετά τους 4 πόντους)
    cpu_speed = 6              # Προεπιλεγμένη ταχύτητα για την κίνηση της CPU (για παλαιότερη συνάρτηση)

    enemy_points, player_points = 0, 0  # Αρχικοποίηση σκορ: και οι δύο ξεκινάνε από 0

    while True:
        # Ενεργοποίηση οριζόντιας κίνησης όταν κάποιος φτάσει 4 πόντους
        allow_horizontal_movement = player_points >= 4 or enemy_points >= 4

        # ========== EVENT HANDLING ==========
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #EVENT ΓΙΑ SOUND ON/OFF
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse clicked at:", event.pos)
                print("Sound icon rect:", sound_icon_rect)
                print("Collides?", sound_icon_rect.collidepoint(event.pos))
                if sound_icon_rect.collidepoint(event.pos):
                    muted = not muted
                    # Εφαρμογή σίγασης/επαναφοράς
                    if muted:
                        pygame.mixer.music.set_volume(0)
                        ball_sound.set_volume(0)
                        point_sound.set_volume(0)
                        game_over_sound.set_volume(0)
                        count_sound.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.8)
                        ball_sound.set_volume(1)
                        point_sound.set_volume(0.3)
                        game_over_sound.set_volume(1)
                        count_sound.set_volume(0.3)            

            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                player.midright = (screen_width, screen_height / 2)

            if game_state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        pygame.mixer.music.stop()
                        music_started = False
                        show_starting_message(screen, screen_width, screen_height, count_sound)
                        game_mode = "1player"
                        game_state = "game"

                    if event.key == pygame.K_2:
                        pygame.mixer.music.stop()
                        music_started = False
                        show_starting_message(screen, screen_width, screen_height, count_sound)
                        game_mode = "2players"
                        game_state = "game"

                    if event.key == pygame.K_3:
                        pygame.mixer.music.stop()
                        music_started = False
                        show_starting_message(screen, screen_width, screen_height, count_sound)
                        game_mode = "cpu_vs_cpu"
                        game_state = "game"

            elif game_state == "game":
                if event.type == pygame.KEYDOWN:
                    if game_mode == "1player":
                        if event.key == pygame.K_UP:
                            player_speed = -5
                        if event.key == pygame.K_DOWN:
                            player_speed = 5
                        if allow_horizontal_movement:
                            if event.key == pygame.K_LEFT:
                                player_speed_x = -3
                            if event.key == pygame.K_RIGHT:
                                player_speed_x = 3

                    elif game_mode == "2players":
                        if event.key == pygame.K_UP:
                            player_speed = -5
                        if event.key == pygame.K_DOWN:
                            player_speed = 5
                        if event.key == pygame.K_w:
                            player2_speed = -5
                        if event.key == pygame.K_s:
                            player2_speed = 5
                        if allow_horizontal_movement:
                            if event.key == pygame.K_LEFT:
                                player_speed_x = -3
                            if event.key == pygame.K_RIGHT:
                                player_speed_x = 3
                            if event.key == pygame.K_a:
                                player2_speed_x = -3
                            if event.key == pygame.K_d:
                                player2_speed_x = 3
                                
        if event.type == pygame.KEYUP:  # Όταν ο παίκτης αφήσει κάποιο πλήκτρο
            if game_mode in ("1player", "2players"):
                if event.key in (pygame.K_UP, pygame.K_DOWN):  # Αν άφησε το πάνω ή κάτω βελάκι
                    player_speed = 0  # Σταματά η κάθετη κίνηση του παίκτη
                if allow_horizontal_movement and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player_speed_x = 0  # Σταματά η οριζόντια κίνηση (αν επιτρέπεται)

            if game_mode == "2players":
                if event.key in (pygame.K_w, pygame.K_s):  # Αν ο 2ος παίκτης άφησε W ή S
                    player2_speed = 0
                if allow_horizontal_movement and event.key in (pygame.K_a, pygame.K_d):  # Αν άφησε A ή D
                    player2_speed_x = 0

        # ========== GAME LOGIC & RENDERING ==========

        if game_state == "menu":
            pygame.mixer.stop()  # Σταματά κάθε ήχος αν βρισκόμαστε στο μενού
            draw_menu(screen, screen_width, screen_height, muted, sound_on_icon, sound_off_icon, sound_icon_rect)

            if not music_started:  # Έναρξη μουσικής εφόσον δεν έχει ξεκινήσει ήδη
                pygame.mixer.music.play(-1)  # Παίζει σε βρόχο (infinite loop)
                music_started = True

        elif game_state == "game":  # Αν παίζουμε
            # Ενημέρωση θέσης μπάλας και έλεγχος για πόντους / σύγκρουση
            ball_speed_x, ball_speed_y, enemy_points, player_points, new_state = animate_ball(
                ball, ball_speed_x, ball_speed_y, screen_width, screen_height,
                player, cpu, enemy_points, player_points, player2, game_mode,
                screen, ball_sound, point_sound, game_over_sound
            )
            game_state = new_state  # Ενημέρωση κατάστασης παιχνιδιού (σε περίπτωση νίκης)

            if game_mode == "1player":
                animate_player(player, player_speed, screen_height)  # Κάθετη κίνηση παίκτη
                if allow_horizontal_movement:
                    animate_player_horizontal(player, player_speed_x, screen_width, ball)  # Οριζόντια κίνηση
                animate_cpu_advanced(cpu, ball, ball_speed_x, ball_speed_y,
                     screen_width, screen_height, 0,  # Θέση εκκίνησης CPU
                     allow_horizontal_movement, False)  # Η CPU είναι στα αριστερά (όχι δεξιά)

            elif game_mode == "2players":
                animate_player(player, player_speed, screen_height)  # Παίκτης 1 (δεξιά)
                animate_player2(player2, player2_speed, screen_height)  # Παίκτης 2 (αριστερά)

                if allow_horizontal_movement:  # Κίνηση στον άξονα Χ
                    animate_player_horizontal(player, player_speed_x, screen_width, ball)
                    animate_player2_horizontal(player2, player2_speed_x, screen_width, ball)

            elif game_mode == "cpu_vs_cpu":
                animate_cpu_advanced(cpu, ball, ball_speed_x, ball_speed_y,
                     screen_width, screen_height, 0,
                     allow_horizontal_movement, False)  # CPU αριστερά
                animate_cpu_advanced(player, ball, ball_speed_x, ball_speed_y,
                     screen_width, screen_height, screen_width - player.width,
                     allow_horizontal_movement, True)  # CPU δεξιά

            # Τελική σχεδίαση όλων στην οθόνη
            draw_game(screen, ball, player, cpu, player2,
                        enemy_points, player_points, screen_width, screen_height, game_mode,
                        muted, sound_on_icon, sound_off_icon, sound_icon_rect)

        pygame.display.update()  # Ενημέρωση οθόνης με τις νέες σχεδιάσεις
        clock.tick(80)  # FPS (ρυθμός ανανέωσης): 80 φορές το δευτερόλεπτο

# Εκτελεί τη main μόνο αν το αρχείο τρέχει ως κύριο πρόγραμμα
if __name__ == "__main__":
    main()