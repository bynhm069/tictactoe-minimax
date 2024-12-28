from tkinter import *
import pygame

# Lớp chính
class TicTacToe:
    def __init__(self, root):
        # Cấu hình cửa sổ chính
        self.root = root
        self.root.geometry("500x500")
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="#dff5e1")  # Nền xanh lá nhạt
        self.root.resizable(0, 0)  # Giữ kích thước cố định

        # Khởi tạo âm thanh
        pygame.mixer.init()
        self.music_playing = False
        self.music_file = "C:/Users/bynh0/OneDrive/Documents/workspace/uef/year3/Artificial intelligence/Hypnotic-Puzzle3.mp3"
        try:
            pygame.mixer.music.load(self.music_file)
        except:
            print("Music file not found or could not be loaded.")

        # Tạo giao diện menu chính
        self.create_main_menu()

# Phần: Giao diện 
    def create_main_menu(self):
        # Xóa các widget hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tiêu đề chính
        titleLabel = Label(self.root, text="Tic Tac Toe", font=("Arial", 32, "bold"), 
                           bg="#2a9d8f", fg="white", width=20, height=2,
                           relief="solid", borderwidth=2, highlightthickness=2, 
                           highlightbackground="white")
        titleLabel.pack(pady=20)

        # Kiểu nút chung
        button_style = {"font": ("Arial", 16, "bold"), "fg": "white", 
                        "width": 18, "height": 2, "borderwidth": 2, 
                        "relief": "solid", "highlightthickness": 2, "highlightbackground": "white"}

        # Nút Singleplayer
        singlePlayerButton = Button(self.root, text="Singleplayer", **button_style,
                                    bg="#6ebf8b", activebackground="#5aa97a", 
                                    command=self.start_single_player) # khi ấn nút sẽ bắt đầu chế độ chơi đơn
        singlePlayerButton.pack(pady=10) # 10 pixel

        # Nút Multiplayer
        multiPlayerButton = Button(self.root, text="Multiplayer", **button_style,
                                   bg="#4a7c59", activebackground="#3c6a4b", 
                                   command=self.start_multi_player)
        multiPlayerButton.pack(pady=10)

        # Nút Settings
        settingsButton = Button(self.root, text="Settings", **button_style,
                                bg="#e76f51", activebackground="#d65c3c", 
                                command=self.open_settings)
        settingsButton.pack(pady=10)

# Phần: Chế độ chơi 
    def start_single_player(self):
        self.mode = "singlePlayer"
        self.start_game()

    def start_multi_player(self):
        self.mode = "multiPlayer"
        self.start_game()

# Phần: Cài đặt 
    def open_settings(self):
        # Xóa giao diện hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tiêu đề cài đặt
        settingsLabel = Label(self.root, text="Settings", font=("Arial", 32, "bold"),
                              bg="#2a9d8f", fg="white", width=20, height=2,
                              relief="solid", borderwidth=2, highlightthickness=2,highlightbackground="white")
        settingsLabel.pack(pady=20)

        # Nút bật/tắt nhạc
        self.musicToggleButton = Button(
            self.root,
            text="Turn Music On" if not self.music_playing else "Turn Music Off",
            width=20,height=2,font=("Arial", 15),bg="#4a7c59",fg="white",relief="solid", activebackground="#3c6a4b",
            command=self.toggle_music,
        )
        self.musicToggleButton.pack(pady=10)

        # Thanh điều chỉnh âm lượng
        volumeLabel = Label(self.root, text="Volume", font=("Arial", 25), bg="#dff5e1")
        volumeLabel.pack(pady=10)

        self.volumeSlider = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, length=200, command=self.adjust_volume) # orient thanh trượt đặt theo chiều
        self.volumeSlider.set(pygame.mixer.music.get_volume() * 100) # Nhân với 100 vì giá trị từ 0.0 đến 1.0
        self.volumeSlider.pack(pady=10) # thêm vào UI

        # Nút trở về menu chính
        backButton = Button(self.root, text="Back to Main Menu", width=20, height=2, font=("Arial", 15), bg="#e76f51", activebackground="#d65c3c", relief="solid", command=self.create_main_menu)
        backButton.pack(pady=20)

    def toggle_music(self): # trạng thái nhạc
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
            self.musicToggleButton.config(text="Turn Music On") # thay đổi hiện thị
        else:
            pygame.mixer.music.play(-1)  # phát nhạc lặp vô hạn
            self.music_playing = True
            self.musicToggleButton.config(text="Turn Music Off")

    def adjust_volume(self, value): #điều chỉnh âm lượng
        volume = int(value) / 100
        pygame.mixer.music.set_volume(volume)

# Phần: Giao diện trò chơi 
    def start_game(self):
        # Xóa giao diện hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tạo giao diện chơi game
        self.frame1 = Frame(self.root, bg="#264653")
        self.frame1.pack(fill=X) # fill=x giúp khung luôn vừa chiều rộng cửa sổ

        #tiêu đề chính
        self.titleLabel = Label(self.frame1, text="Tic Tac Toe", font=("Arial", 32, "bold"), bg="#2a9d8f", fg="white",
                                width=16, relief="solid", 
                                borderwidth=2, highlightthickness=2, highlightbackground="white",anchor="center")
        self.titleLabel.grid(row=0, column=0, sticky="nsew")

        #đặt timer
        self.timerLabel = Label(self.frame1, text="Time: 60s", font=("Arial", 22, "bold"), bg="#264653", fg="white",
                            relief="solid", borderwidth=2, highlightthickness=2, highlightbackground="white")
        self.timerLabel.grid(row=0, column=1, sticky="nsew")

        self.time_left = 60  # Cài đặt thời gian đếm ngược 60 giây
        self.timer_running = True
        self.update_timer()

        #Xác định cột bố cục
        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)

        self.optionFrame = Frame(self.root, bg="grey")
        self.optionFrame.pack() # căn chỉnh tự động

        self.frame2 = Frame(self.root, bg="#dff5e1")
        self.frame2.pack()

        self.board = {1: " ", 2: " ", 3: " ",
                      4: " ", 5: " ", 6: " ",
                      7: " ", 8: " ", 9: " "}

        self.turn = "x" # người chơi x bắt đầu trước
        self.game_end = False # nghĩa là trò chơi vẫn đang diễn ra, true là kết thúc

        self.create_game_buttons()

        # Nút Restart
        self.restartButton = Button(self.frame2, text="Restart Game", width=19, height=2, font=("Arial", 20), bg="#6ebf8b", activebackground="#5aa97a", relief="solid", command=self.restart_game)
        self.restartButton.grid(row=4, column=0, columnspan=3)

        # Nút Back
        self.back_icon = PhotoImage(file="pngtree-back-arrow-backward-direction-previous-png-image_5198415.png").subsample(8, 8)
        self.returnButton = Button(self.frame1,image=self.back_icon,
            bg="#2a9d8f",activebackground="#2a9d8f",relief="flat",borderwidth=0,
            command=self.create_main_menu
        )
        self.returnButton.grid(row=0, column=0, padx=10, pady=8, sticky="w")

    def update_timer(self):
        if self.time_left > 0 and self.timer_running:
            self.time_left -= 1

            # Thay đổi màu chữ khi thời gian gần hết
            if self.time_left <= 10:
                self.timerLabel.config(fg="red")
            else:
                self.timerLabel.config(fg="white")

            # Hiệu ứng chớp nháy
            if self.time_left <= 5 and self.time_left % 2 == 0:
                self.timerLabel.config(bg="#F4A261")  # Màu nền cảnh báo
            else:
                self.timerLabel.config(bg="#264653")  # Màu nền mặc định

            # cập nhật nội dung nhãn
            self.timerLabel.config(text=f"Time: {self.time_left}s")
            # sau 1s là giảm thời gian (1000ms = 1s)
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0 and not self.game_end: #điều kiện dừng vòng lặp
            # Thông báo khi hết giờ
            self.timerLabel.config(text="Time's up!", fg="red")
            self.end_game("It's a draw!")

    def create_game_buttons(self): # tạo khung đánh
        self.buttons = []
        for i in range(3): # tạo lưới 3x3
            for j in range(3):
                button = Button(self.frame2, text=" ", width=10, height=4, font=("Arial", 16), bg="white", fg="black", relief="solid", borderwidth=1,highlightthickness=2)
                button.grid(row=i, column=j, padx=1, pady=1)
                button.bind("<Button-1>", self.play)
                self.buttons.append(button)

    def update_board(self):
        for key in self.board.keys():
            self.buttons[key - 1]["text"] = self.board[key]

    def check_for_win(self, player): # điều kiện dòng thắng
        return ((self.board[1] == self.board[2] == self.board[3] == player) or
                (self.board[4] == self.board[5] == self.board[6] == player) or
                (self.board[7] == self.board[8] == self.board[9] == player) or
                (self.board[1] == self.board[4] == self.board[7] == player) or
                (self.board[2] == self.board[5] == self.board[8] == player) or
                (self.board[3] == self.board[6] == self.board[9] == player) or
                (self.board[1] == self.board[5] == self.board[9] == player) or
                (self.board[3] == self.board[5] == self.board[7] == player))

    def check_for_draw(self): # điều kiện hòa
        return all(self.board[i] != " " for i in self.board) 

    def play(self, event):
        if self.game_end:
            return
        
        #lấy thông tin từ nút
        button = event.widget
        clicked = self.buttons.index(button) + 1

        # cập nhật trạng thái ô
        if button["text"] == " ":
            self.board[clicked] = self.turn
            self.update_board()

            if self.check_for_win(self.turn):
                self.end_game(f"{self.turn.upper()} wins!")
                return

            if self.check_for_draw():
                self.end_game("It's a draw!")
                return

            self.turn = "o" if self.turn == "x" else "x" # đổi lượt chơi

            if self.mode == "singlePlayer" and self.turn == "o":
                self.play_computer()
                self.update_board()
                if self.check_for_win(self.turn):
                    self.end_game(f"{self.turn.upper()} wins!")
                if self.check_for_draw() and not self.game_end:
                    self.end_game("It's a draw!")
                self.turn = "x"

    def play_computer(self):
        bestScore = -100 
        bestMove = 0
        for key in self.board.keys():
            if self.board[key] == " ":
                self.board[key] = "o"
                score = self.minimax(self.board, False) # tham số false cho biết lượt tiếp theo là của đối thủ
                self.board[key] = " "
                if score > bestScore:
                    bestScore = score
                    bestMove = key
        self.board[bestMove] = "o"

    def minimax(self, board, isMaximizing):
        if self.check_for_win("o"):
            return 1
        if self.check_for_win("x"):
            return -1
        if self.check_for_draw():
            return 0
        
        # Giai đoạn tối đa hóa
        if isMaximizing:
            bestScore = -100
            for key in board.keys():
                if board[key] == " ":
                    board[key] = "o"
                    score = self.minimax(board, False)
                    board[key] = " "
                    bestScore = max(score, bestScore)
            return bestScore
        else: # giai đoạn tối thiểu hóa (tìm điểm bất lợi cho máy)
            bestScore = 100
            for key in board.keys():
                if board[key] == " ":
                    board[key] = "x"
                    score = self.minimax(board, True)
                    board[key] = " "
                    bestScore = min(score, bestScore)
            return bestScore

    def restart_game(self): # reset khi kết thúc 1 hiệp
        self.game_end = False
        self.turn = "x"
        self.time_left = 60
        self.timer_running = True
        self.update_timer()
        for button in self.buttons:
            button["text"] = " "
        for i in self.board.keys():
            self.board[i] = " "
        self.update_board()
        self.titleLabel.config(text="Tic Tac Toe")

    def end_game(self, message):
        self.timer_running = False
        self.titleLabel.config(text=message)
        self.game_end = True

#Chạy ứng dụng
if __name__ == "__main__":
    root = Tk()
    game = TicTacToe(root)
    root.mainloop()
