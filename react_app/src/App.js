import './App.css';
import React, { useState, useEffect, useRef } from 'react';

/* function Chessboard() {
  const numberOfRows = 9;
  const numberOfFields = numberOfRows * numberOfRows;
  const [clicked, setClicked] = useState(Array(numberOfFields).fill(false));
  const checkedRef = useRef(clicked);

  const handleCheckboxClick = (index) => {
    // If none of the checkboxes are clicked, set the clicked state for the clicked checkbox to true
    if (clicked.every((val) => val === false)) {
      const newClicked = [...clicked];
      newClicked[index] = true;
      setClicked(newClicked);
    }
    else {
      console.log('Checkbox clicked');
      let newClicked = clicked;
      let prevClicked = clicked.indexOf(true);
      newClicked[prevClicked] = false;
      console.log(newClicked[prevClicked]);
      setClicked(newClicked);
    }
    console.log(clicked);
    checkedRef = clicked;
  };

  const renderCell = (index) => {
    return (
      <td key={index}>
        <input
          type="checkbox"
          onClick={() => handleCheckboxClick(index)}
          // checked={clicked[index]}
          checked = {checkedRef[index]}
        />
      </td>
    );
  };

  const renderRow = (startIndex) => {
    const cells = [];
    for (let i = startIndex; i < startIndex + numberOfRows; i++) {
      cells.push(renderCell(i));
    }
    return <tr key={startIndex}>{cells}</tr>;
  };

  const renderBoard = () => {
    const rows = [];
    for (let i = 0; i < numberOfFields; i += numberOfRows) {
      rows.push(renderRow(i));
    }
    return (
      <table>
        <tbody>{rows}</tbody>
      </table>
    );
  };

  return <div>{renderBoard()}</div>;
} */


function App() {
  const inputMoveRef = useRef();
  const [flaskState, setFlaskState] = useState([]);

  const numberOfRows = 9;
  const numberOfFields = numberOfRows * numberOfRows;
  const [checked, setChecked] = useState(Array(numberOfFields).fill(false));
  const [prevChecked, setPrevChecked] = useState(-1);
  const [moveMade, setMoveMade] = useState(true);

  const keysToMove = [
    "A9", "B9", "C9", "D9", "E9", "F9", "G9", "H9", "I9",
    "A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8", "I8",
    "A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7", "I7",
    "A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6", "I6",
    "A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5", "I5",
    "A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4", "I4",
    "A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3", "I3",
    "A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2", "I2",
    "A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1",
  ];

  const sendMove = () => {
    console.log(keysToMove[checked.indexOf(true)]);
    const inputMove = inputMoveRef.current.value;
    fetch('http://127.0.0.1:5000/uttt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ move: inputMove })
    })
      .then(response => response.json())
      .then(data => console.log(data.message));
    inputMoveRef.current.value = null;
  };

  const receiveMove = () => {
    fetch('http://127.0.0.1:5000/uttt', {
      method: 'GET'
    })
      .then(response => response.json())
      .then(data => setFlaskState([data.state.move, data.state.isOver]));
  };

  function MoveDisplay() {
    return flaskState !== null ? <p>Received move: {flaskState}</p> : null;
  }

  // function CheckboxGrid() {
  //   return (
  //     <div>
  //       {renderGrid()}
  //     </div>
  //   );
  // }

  // useEffect(() => {
  //   if (moveMade) {
  //     setPrevChecked(-1);
  //   }
  // }, [moveMade]);

  // const handleCheckboxClick = (index) => {
  //   if (moveMade) {
  //     const newChecked = [...checked];
  //     newChecked[index] = !checked[index];
  //     setChecked(newChecked);

  //     if (prevChecked !== -1 && prevChecked !== index) {
  //       newChecked[prevChecked] = false;
  //       setChecked(newChecked);
  //     }
  //     setPrevChecked(index);
  //   }
  // };

  // const renderCheckbox = (index) => {
  //   /* return (
  //     <div key={index}>
  //       <input
  //         type="checkbox"
  //         onClick={() => handleCheckboxClick(index)}
  //         checked={checked[index]}
  //         disabled={!moveMade}
  //       />
  //       <label>Checkbox {index}</label>
  //     </div>
  //   ); */
  //   return (
  //     <td key={index}>
  //       <button
  //         type="checkbox"
  //         onClick={() => handleCheckboxClick(index)}
  //         checked = {checked[index]}
  //         disabled={!moveMade}
  //       >{keysToMove[index]}</button>
  //     </td>
  //   );
  // };

  // const renderRow = (startIndex) => {
  //   const cells = [];
  //   for (let i = startIndex; i < startIndex + numberOfRows; i++) {
  //     cells.push(renderCheckbox(i));
  //   }
  //   return <tr key={startIndex}>{cells}</tr>;
  // };

  // const renderGrid = () => {
  //   const rows = [];
  //   for (let i = 0; i < numberOfFields; i += numberOfRows) {
  //     rows.push(renderRow(i));
  //   }
  //   return (
  //     <table>
  //       <tbody>{rows}</tbody>
  //     </table>
  //   );
  // };

  function ButtonGrid() {
    const [selectedButton, setSelectedButton] = useState(null);
  
    const handleButtonClick = (value) => {
      if (value === selectedButton) {
        // If the same button is clicked again, unselect it
        setSelectedButton(null);
      } else {
        // Otherwise, select the new button and unselect the previously selected one
        setSelectedButton(value);
      }
    };
  
    const renderButton = (value) => {
      return (
        <button
          key={value}
          onClick={() => handleButtonClick(value)}
          className={selectedButton === value ? "selected" : ""}
          disabled={!moveMade}
        >
          {value}
        </button>
      );
    };
  
    const renderRow = (startIndex) => {
      const buttons = [];
      for (let i = startIndex; i < startIndex + 4; i++) {
        buttons.push(renderButton(i));
      }
      return <div key={startIndex}>{buttons}</div>;
    };
  
    const renderGrid = () => {
      const rows = [];
      for (let i = 0; i < 16; i += 4) {
        rows.push(renderRow(i));
      }
      return <div>{rows}</div>;
    };
  
    return <div>{renderGrid()}</div>;
  }

  return (
    <>
      {/* <table className="big_table live">
        <tr className="1">
            <td className="1">
                <table className="little_table col-1 row-1">
                    <tr className="1">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="2">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="3">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                </table>
            </td>
            <td className="2">
                <table className="little_table col-2 row-1">
                    <tr className="1">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="2">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="3">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                </table>
            </td>
            <td className="3">
                <table className="little_table col-3 row-1">
                    <tr className="1">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="2">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="3">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr className="2">
            <td className="1">
                <table className="little_table col-1 row-2">
                    <tr className="1">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="2">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="3">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                </table>
            </td>
            <td className="2">
                <table className="little_table col-2 row-2">
                    <tr className="1">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="2">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="3">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                </table>
            </td>
            <td className="3">
                <table className="little_table col-3 row-2">
                    <tr className="1">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="2">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="3">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr className="3">
            <td className="1">
                <table className="little_table col-1 row-3">
                    <tr className="1">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="2">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="3">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                </table>
            </td>
            <td className="2">
                <table className="little_table col-2 row-3">
                    <tr className="1">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="2">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="3">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                </table>
            </td>
            <td className="3">
                <table className="little_table col-3 row-3">
                    <tr className="1">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="2">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                    <tr className="3">
                        <td className="1 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="2 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                        <td className="3 "><div className="cellDiv"><input type="checkbox"></input></div></td>
                    </tr>
                </table>
            </td>
        </tr>
      </table> */}
      <div id="inputDiv">
        {/* <CheckboxGrid /> */}
        <ButtonGrid />
        <label htmlFor="move-input">Enter a move:</label>
        <input type="text" ref={inputMoveRef} /* value={inputMove} */ /* onChange={handleInputChange} */ />
        <button onClick={sendMove}>Send</button>
        <button onClick={receiveMove}>Receive (basically redundant jer se odma dvaput poziva GET request na flask (nije jos))</button>
        <MoveDisplay />
      </div>
    </>
  );
}

export default App;
