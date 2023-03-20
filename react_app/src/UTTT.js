import './UTTT.css';
import React, { useState, useEffect, useRef } from 'react';

function UTTT () {
  const gameID = Math.random();
  const boardsRef = useRef([]);
  const buttonsRef = useRef([]);
  const inputRef = useRef({value: 23});
  const spanRef = useRef(null);
  const optionsRef = useRef(null);
  const userSymbolRef = useRef(null);
  let userSymbol = "symbolO";
  let AiSymbol = "symbolX";
  let tieSymbol = "symbolTie";
  let optionsVisibility = false;

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
    console.log("sent num iters:", inputRef.current.value);
    const button = buttonsRef.current[index];
    const inClassName = (str) => { return button.className.includes(str) };
    console.log("buttons", buttonsRef);
    console.log("boards", boardsRef);
    if (!inClassName('empty') || !inClassName('enabled')) {
      return;
    }
    
    button.className = button.className.replace('empty', userSymbol);
    const move = keysToMove[index];
    disableAllBoards();
    console.log("Sent move:", move);
    sendMove(move);
  }

  const sendMove = (move) => {
    fetch('https://bornagojsic.pythonanywhere.com/uttt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: gameID, move: move, numIters: getInputNum() })
    })
      .then(response => response.json())
      .then(data => {
        // ovo stavit u novu funkciju handleData
        
        console.log("Gotten:", data);
        boardWinners = data.boardWinners;

        if (data.isOver !== "false") {
          if (data.move === "") {
            // the player has won
            showBoardWinner(userSymbol, Math.floor(moveToKeys[move] / 9));
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
        button.className = button.className.replace('empty', AiSymbol);
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
        // treba bolja implementacija ovo neka fja npr
        if (boardWinners[Math.floor(moveKey / 9)] === "x") {
          showBoardWinner(AiSymbol, Math.floor(moveKey / 9));
        }
        if (boardWinners[Math.floor(moveToKeys[move] / 9)] === "o") {
          showBoardWinner(userSymbol, Math.floor(moveToKeys[move] / 9));
        }
        if (boardWinners[Math.floor(moveKey / 9)] === "f") {
          showBoardWinner(tieSymbol, Math.floor(moveKey / 9));
        }
        if (boardWinners[Math.floor(moveToKeys[move] / 9)] === "f") {
          showBoardWinner(tieSymbol, Math.floor(moveToKeys[move] / 9));
        }

        if (data.isOver !== "false") {
          // the AI has won
          // this next line is redundant but this all isOver needs its own function
          showBoardWinner(AiSymbol, Math.floor(moveKey / 9)); 
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
  //     boardsRef.current[i].className = boardsRef.current[i].className.replace("symbolX", "winner");
  //     boardsRef.current[i].className = boardsRef.current[i].className.replace("symbolO", "winner");
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
        squares: Array(9).fill(null),
        winner: null,
        })
      );
    
    console.log(boards);

    // render the boards
    return (
      <div id="container">
        <div className="table" id="big-board">
          {boards.map((board, boardIndex) => (
            <div className="board" key={`board-${boardIndex}`}>
              <TicTacToeBoard
                key={`ttt-board-${boardIndex}`}
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
        <div className="winner" key={`winnerdiv-${boardIndex}`} ref={el => (boardsRef.current[boardIndex] = el)} />
        <div className="little-table" key={`little-table-${boardIndex}`}>
          {board.squares.map((square, index) => (
            <div className="square" key={`square-div-${index}`}>
              <Square
                key={`square-${index}`}
                value={undefined}
                onClick={() => onClick(9 * boardIndex + index)}
                index={9 * boardIndex + index}
              />
            </div>
          ))}
        </div>
      </>
    );
  };

  const Square = ({ value, onClick, index }) => {
    // render the square with the appropriate value and click handler
    return (
      <button key={`button-${index}`} className="empty enabled userO" onClick={onClick} ref={el => (buttonsRef.current[index] = el)}>
        {value}
      </button>
    );
  };

  const handleSliderChange = () => {
    // console.log(getInputNum());
    spanRef.current.innerHTML = `Number of simulations: ${getInputNum()}`;
  }

  const Slider = () => {
    return (
      <div id="slider" key="slider-div">
        <span ref={spanRef}>
          Number of simulations: {getInputNum()}
        </span>
        <input type="range" className='slider' min="0" max="37" onChange={handleSliderChange} defaultValue={inputRef.current.value} ref={inputRef}/>
        <span>
          Note: The waiting time for the AI's move is larger for more simulations
        </span>
      </div>
    );
  };

  const inputKeys = [
    '1',
    '10', '20', '30', '40', '50', '60', '70', '80', '90',
    '100', '200', '300', '400', '500', '600', '700', '800', '900',
    '1000', '2000', '3000', '4000', '5000', '6000', '7000', '8000', '9000',
    '10000', '20000', '30000', '40000', '50000', '60000', '70000', '80000', '90000',
    '100000'
  ];

  const getInputNum = () => {
    return inputKeys[inputRef.current.value];
  };

  const showOptions = () => {
    if (optionsVisibility === true) {
      optionsRef.current.style = "visibility: hidden";
    } else {
      optionsRef.current.style = "visibility: visible";
    }
    optionsVisibility = !optionsVisibility;
  };

  const switchSymbols = (element, symbol, newSymbol) => {
    if (element.className.includes(symbol)) {
      element.className = element.className.replace(symbol, newSymbol);
    } else {
      element.className = element.className.replace(newSymbol, symbol);
    }
  };

  const changeUserSymbol = () => {
    switchSymbols(userSymbolRef.current, "O", "X");
    buttonsRef.current.forEach(button => {
      switchSymbols(button, "symbolO", "symbolX");
      switchSymbols(button, "userO", "userX");
    });
    boardsRef.current.forEach(board => {
      switchSymbols(board, "symbolO", "symbolX");
    });
    [userSymbol, AiSymbol] = [AiSymbol, userSymbol];
  };

  const Options = () => {
    return (
      <div id="options" ref={optionsRef}>
        <div id="options-button-container">
          <button id="options-button" onClick={showOptions}></button>
        </div>
        <div id="options-container">
          <button className={`options O`} ref={userSymbolRef} onClick={changeUserSymbol}></button>
        </div>
      </div>
    );
  };

  return (
    <>
      <Board />
      <Slider />
      <Options />
    </>
  );
}

export default UTTT;