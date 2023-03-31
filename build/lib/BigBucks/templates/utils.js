const SERVER_ORIGIN = 'http://127.0.0.1:5000/';


// const loginUrl = `${SERVER_ORIGIN}/login`;


// export const login = (credential) => {
//   return fetch(loginUrl, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     credentials: 'include',
//     body: JSON.stringify(credential)
//   }).then((response) => {
//     if (response.status !== 200) {
//       throw Error('Fail to log in');
//     }


//     return response.json();
//   })
// }


// const registerUrl = `${SERVER_ORIGIN}/register`;


// export const register = (data) => {
//   return fetch(registerUrl, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify(data)
//   }).then((response) => {
//     if (response.status !== 200) {
//       throw Error('Fail to register');
//     }
//   })
// }


// const logoutUrl = `${SERVER_ORIGIN}/logout`;


// export const logout = () => {
//   return fetch(logoutUrl, {
//     method: 'POST',
//     credentials: 'include',
//   }).then((response) => {
//     if (response.status !== 200) {
//       throw Error('Fail to log out');
//     }
//   })
// }

const searchStockByIdUrl = `${SERVER_ORIGIN}/searchById?stock_id=`;


export const searchStockById = (stockId) => {
  return fetch(`${searchStockByIdUrl}${stockId}`).then((response) => {
    if (response.status !== 200) {
      throw Error('Fail to find the stock');
    }
    return response.json();
  })
}

const searchStockByNameUrl = `${SERVER_ORIGIN}/searchByName?stock_id=`;

export const searchStockByName = (stockName) => {
  return fetch(`${searchStockByNameUrl}${stockName}`).then((response) => {
    if (response.status !== 200) {
      throw Error('Fail to find the stock');
    }
    return response.json();
  })
}


const tradeStockUrl = `${SERVER_ORIGIN}/favorite`;


export const buyStock = (buyData) => {
  return fetch(tradeStockUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(buyData)
  }).then((response) => {
    if (response.status !== 200) {
      throw Error('Fail to buy in');
    }
})
}


export const sellStock = (sellData) => {
  return fetch(tradeStockUrl, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(sellData)
  }).then((response) => {
    if (response.status !== 200) {
      throw Error('Fail to sold out');
    }
})
}


export const getPortfolio = () => {
  return fetch(tradeStockUrl, {
    credentials: 'include',
  }).then((response) => {
    if (response.status !== 200) {
      throw Error('Fail to get portfilio');
    }


    return response.json();
  })
}
