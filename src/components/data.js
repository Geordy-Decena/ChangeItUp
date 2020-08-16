import React, { useState, useEffect, Fragment } from 'react';
import '../App.css';
import { Transition } from 'react-transition-group'



function Data() {

    const [isData, setData] = useState({})
    const [isUrl, setUrl] = useState({
        url: "",
        valid: false
    })

    function handleChange(e) {
        setUrl({ url: `${e.target.value}` })
    }

    function checkUrl() {
        if (isUrl.url === "") {
            setUrl({ ...isUrl, valid: 1 })
        }
        else {
            setUrl({ ...isUrl, valid: true })
        }
    }

    return (
        <Fragment>
            <div className="background">
            </div>
            <div className="bgImageContainer">
                <img src="https://images.freeimages.com/images/large-previews/cea/this-is-a-macro-snap-of-some-twenty-dollar-bills-1491818.jpg" className="bgImage"></img>
            </div>
            <div className="header">
                <h1>Change it up</h1>
                <h2>Simply enter in a url image of coins (Canadian) and your change will be calculated for you!</h2>
                <div></div>
            </div>
            <div className="form">
                <div className="label" for="name">Url</div>
                <input className="input" type="text" name="url" onChange={(e) => handleChange(e)} />
            </div>
            <div className="btnContainer">
                <button onClick={() => {
                    checkUrl()
                    var url = "https://i.ibb.co/5Mrq2jd/coins7.jpg"
                    url = String(isUrl.url)
                    const response = fetch('/add_url', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(url)
                    }).then(res => res.json()).then(data => setData(data))
                    if (response.ok) {
                        console.log("it worked")
                    }
                }
                } className="button">Evaluate Change</button>
            </div>
            {(isUrl.valid === true) && (
                <Fragment>
                    <Transition
                        timeout={8000}
                        in={true}
                        appear
                    >{(status) => (
                        <div className={`resultsContainer resultsContainer-${status}`}>
                            <div className="imgContainer">
                                <img src={isUrl.url} className="image"></img>
                            </div>
                            <h1>Amount: <h1>{`$${isData.value}`}</h1></h1>
                            <h3>{`x${isData.toonies}`} Toonies</h3>
                            <h3>{`x${isData.loonies}`} Loonies</h3>
                            <h3>{`x${isData.quarters}`} Quarters</h3>
                            <h3>{`x${isData.nickels}`} Nickels</h3>
                            <h3>{`x${isData.dimes}`} Dimes</h3>
                        </div>
                    )}
                    </Transition>
                    <Transition
                        timeout={8000}
                        in={true}
                        appear
                    >{(status) => (
                        <div className={`loading loading-${status}`}>
                            Loading...
                        </div>
                    )}
                    </Transition>
                </Fragment>
            )}
            {(isUrl.valid === 1) && (
                <Fragment>
                    <div className="urlWarning">Please enter a URL</div>
                </Fragment >
            )}
        </Fragment >
    );
}

export default Data;
