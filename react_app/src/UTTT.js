import './App.css';
import './UTTT.css';
import React, { useState, useEffect, useRef } from 'react';

function UTTT () {
  const gameID = Math.random();
  const boardsRef = useRef([]);
  const buttonsRef = useRef([]);

  const keysToMove = [
    "A9", "B9", "C9", "A8", "B8", "C8", "A7", "B7", "C7",
    "D9", "E9", "F9", "D8", "E8", "F8", "D7", "E7", "F7",
    "G9", "H9", "I9", "G8", "H8", "I8", "G7", "H7", "I7",
    "A6", "B6", "C6", "A5", "B5", "C5", "A4", "B4", "C4",
    "D6", "E6", "F6", "D5", "E5", "F5", "D4", "E4", "F4",
    "G6", "H6", "I6", "G5", "H5", "I5", "G4", "H4", "I4",
    "A3", "B3", "C3", "A2", "B2", "C2", "A1", "B1", "C1",
    "D3", "E3", "F3", "D2", "E2", "F2", "D1", "E1", "F1",
    "G3", "H3", "I3", "G2", "H2", "I2", "G1", "H1", "I1",
  ];

  let moveToKeys = {
    "A9":  0, "B9":  1, "C9":  2, "A8":  3, "B8":  4, "C8":  5, "A7":  6, "B7":  7, "C7":  8,
    "D9":  9, "E9": 10, "F9": 11, "D8": 12, "E8": 13, "F8": 14, "D7": 15, "E7": 16, "F7": 17,
    "G9": 18, "H9": 19, "I9": 20, "G8": 21, "H8": 22, "I8": 23, "G7": 24, "H7": 25, "I7": 26,
    "A6": 27, "B6": 28, "C6": 29, "A5": 30, "B5": 31, "C5": 32, "A4": 33, "B4": 34, "C4": 35,
    "D6": 36, "E6": 37, "F6": 38, "D5": 39, "E5": 40, "F5": 41, "D4": 42, "E4": 43, "F4": 44,
    "G6": 45, "H6": 46, "I6": 47, "G5": 48, "H5": 49, "I5": 50, "G4": 51, "H4": 52, "I4": 53,
    "A3": 54, "B3": 55, "C3": 56, "A2": 57, "B2": 58, "C2": 59, "A1": 60, "B1": 61, "C1": 62,
    "D3": 63, "E3": 64, "F3": 65, "D2": 66, "E2": 67, "F2": 68, "D1": 69, "E1": 70, "F1": 71,
    "G3": 72, "H3": 73, "I3": 74, "G2": 75, "H2": 76, "I2": 77, "G1": 78, "H1": 79, "I1": 80,
  };

  let boardWinners = Array(9).fill('.');
  let nextPlayerBoard = -1;
  // let gameOver = false;

  const boardClassNameReplace = (boardIndex, name, replaceWith) => {
    boardsRef.current[boardIndex].className = boardsRef.current[boardIndex].className.replace(name, replaceWith);
  }

  const handleClick = async (index) => {
    console.log(index);
    const button = buttonsRef.current[index];
    const inClassName = (str) => { return button.className.includes(str) };
    console.log("buttons", buttonsRef);
    console.log("boards", boardsRef);
    if (!inClassName('empty') || !inClassName('enabled')) {
      return;
    }
    
    button.className = button.className.replace('empty', 'O');
    const move = keysToMove[index];
    disableAllBoards();
    console.log("Sent move:", move);
    sendMove(move);


  }

  const sendMove = (move) => {
    fetch('http://bornagojsic.pythonanywhere.com/uttt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: gameID, move: move })
    })
      .then(response => response.json())
      .then(data => {
        // ovo stavit u novu funkciju handleData
        
        console.log("Gotten:", data);
        boardWinners = data.boardWinners;

        if (data.isOver !== "false") {
          if (data.move === "") {
            // the player has won
            showBoardWinner("O", Math.floor(moveToKeys[move] / 9));
            console.log("GAME OVER!");
            alert('Game Over!');
            for (let i = 0; i < 9; i++) {
              disableBoard(i);
            }
            return;
            // gameOver = true;
          }
        }
        
        const moveKey = moveToKeys[data.move];
        const button = buttonsRef.current[moveKey];
        button.className = button.className.replace('empty', 'X');
        nextPlayerBoard = moveKey % 9;
        console.log("next move must be on board:", nextPlayerBoard);
        console.log("boardwinners:", boardWinners, Math.floor(moveKey / 9), Math.floor(moveToKeys[move] / 9));
        // if the board is not won yet, then you can put a symbol only on
        // that board, you can put it on any non-won board
        if (boardWinners[nextPlayerBoard] === ".") {
          console.log("only this board!");
          enableBoard(nextPlayerBoard);
        } else {
          enableAllNonWonBoards();
        }
        // checks for won boards
        if (boardWinners[Math.floor(moveKey / 9)] !== ".") {
          showBoardWinner("X", Math.floor(moveKey / 9));
        }
        if (boardWinners[Math.floor(moveToKeys[move] / 9)] !== ".") {
          showBoardWinner("O", Math.floor(moveToKeys[move] / 9));
        }

        if (data.isOver !== "false") {
          // the AI has won
          // this next line is redundant but this all isOver needs its own function
          showBoardWinner("X", Math.floor(moveKey / 9)); 
          console.log("GAME OVER!");
          alert('Game Over!');
          for (let i = 0; i < 9; i++) {
            disableBoard(i);
          }
          return;
          // gameOver = true;
        }
      });
  };

  const handleData = (data) => {};

  const showBoardWinner = (symbol, boardIndex) => {
    boardClassNameReplace(boardIndex, "winner", symbol);
  }

  // const removeBoardWinners = () => {
  //   for (let i = 0; i < 9; i++) {
  //     boardsRef.current[i].className = boardsRef.current[i].className.replace("X", "winner");
  //     boardsRef.current[i].className = boardsRef.current[i].className.replace("O", "winner");
  //   }
  // }

  const disableAllBoards = () => {
    for (let i = 0; i < 9; i++) {
      disableBoard(i);
    }
  }

  const disableBoard = (boardIndex) => {
    for (let i = 0; i < 9; i++) {
      const button = buttonsRef.current[boardIndex * 9 + i];
      button.className = button.className.replace('enabled', 'disabled');
    }
  }

  const enableAllNonWonBoards = () => {
    for (let i = 0; i < 9; i++) {
      if (boardWinners[i] === ".") {
        enableBoard(i);
      }
    }
  };

  const enableBoard = (boardIndex) => {
    for (let i = 0; i < 9; i++) {
      const button = buttonsRef.current[boardIndex * 9 + i];
      button.className = button.className.replace('disabled', 'enabled');
    }
  }

  const Board = () => {
    // create an array to represent the 3x3 grid of Tic Tac Toe boards
    const boards = Array(9)
      .fill(null)
      .map(() => ({
        rows: Array(3)
          .fill(null)
          .map(() => 
            Array(3).fill(null)
          ),
        winner: null,
        })
      );
    
    console.log(boards);

    // render the boards
    return (
      <div id="container">
        <div className="table" id="big-board">
          {boards.map((board, boardIndex) => (
            <div className="board" key={boardIndex}>
              <TicTacToeBoard
                    key={boardIndex}
                    board={board}
                    onClick={(index) => handleClick(index)}
                    boardIndex={boardIndex}
                  />
            </div>
          ))}
        </div>
      </div>
    );
  };

  const TicTacToeBoard = ({ board, onClick, boardIndex }) => {
    // render the squares
    return (
      <>
        <div className="winner" key={(boardIndex + 1) * 9} ref={el => (boardsRef.current[boardIndex] = el)} />
        <table className="little-board" key={boardIndex}>
          <thead/>
          <tbody>
            {board.rows.map((row, rowIndex) => (
              <tr className="little-board-row" key={rowIndex}>
                {row.map((col, colIndex) => (
                  <td className={`little-board-col little-board-col-${3 * rowIndex + colIndex}`} key={colIndex}>
                    <Square
                      key={3 * rowIndex + colIndex}
                      value={undefined}
                      onClick={() => onClick(9 * boardIndex + 3 * rowIndex + colIndex)}
                      index={9 * boardIndex + 3 * rowIndex + colIndex}
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
          <tfoot/>
        </table>
      </>
    );
  };

  const Square = ({ value, onClick, index }) => {
    // render the square with the appropriate value and click handler
    return (
      <button className="empty enabled" onClick={onClick} ref={el => (buttonsRef.current[index] = el)}>
        {value}
      </button>
    );
  };

  return (
    <Board />
  );
}

export default UTTT;