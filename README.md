# VisionChess
The VisionChess project is system that applies computer vision techniques and algorithms to capture a game of chess played in the real world and accurately analyze what moves were made. Through a camera positioned above a stationary chess board, the system aims to output a virtual depiction of a game of Chess played in real-time in the physical world by two players.
![Alt text](/Screenshots/detected_all_pieces.png?raw=true "Running Chess Vision Application")
##### * Images for my chess demo show first move being made by black instead of white,however this is illegal in normal chess game.Our System is currently just tracing movement of pieces from initial state,However it will be a interesting extension of this project to combine it with chess engines like stockfish. *
## Getting Started

Download or clone this repository to your local system.You need to have an external camera attached to your system as well as chess game to have a demo.

### Prerequisites

You need to install Opencv on your machine. This project has been tested on Ubuntu 16.04 with OpenCV 2.4.13.Installing OpenCV on ubuntu has been documented in my repositories.

### Installing
Download this project to your machine.
Move to the folder using
```
cd VisionChess
```
And run it using
```
sudo python main.py
```
### Some Screenshots from working application
![Alt text](/Screenshots/digital_chess_board.png?raw=true "Digital Chess Board")
![Alt text](/Screenshots/Move1_frame.png?raw=true "Move 1 on board")

## Authors

* **Amanpreet Walia** - *Chess Vision Algorithm* 
* **Youn Sun (Joy) Choi** - *Implemented chess board* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

