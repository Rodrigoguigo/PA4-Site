import pyrebase

class DbUser:

    _config = {
        "apiKey": "AIzaSyDRM9I3jgbfildmM4XBgG8CcBcTe9VqeC4",
        "authDomain": "mucha-pizza.firebaseapp.com",
        "databaseURL": "https://mucha-pizza.firebaseio.com",
        "projectId": "mucha-pizza",
        "storageBucket": "mucha-pizza.appspot.com",
        "messagingSenderId": "512215867371"
    }
    _firebase = pyrebase.initialize_app(_config)
    _auth = _firebase.auth()
    _db = _firebase.database()
    currentUser = False

    def userLogin(self, email, password):
        try:
            self.currentUser = self._auth.sign_in_with_email_and_password(email, password)
        except:
            self.currentUser = False
    
    def isUserLoggedIn(self):
        if not self.currentUser:
            return self.currentUser
        else:
            return True
    
    def createPizza(self, pizza, values):
        pizzas = self._db.child('pizzas').get(self.currentUser['idToken']).val()
        if pizza in pizzas:
            return "Pizza já cadastrada!"
        else:
            self._db.child('pizzas').child(pizza).set(values, self.currentUser['idToken'])
            return "Pizza cadastrada com sucesso"

    def updatePizza(self, pizza, values):
        self._db.child('pizzas').child(pizza).update(values, self.currentUser['idToken'])

    def deletePizza(self, pizza):
        self._db.child('pizzas').child(pizza).remove(self.currentUser['idToken'])
    
    def deletePedido(self, pedido):
        self._db.child('pedidos').child(pedido).remove(self.currentUser['idToken'])
