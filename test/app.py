from fusion import Web

app = Web.App()

app.router.add_get("")
app.router.add_post("")

if __name__ == '__main__':
    Web.run(app, host='0.0.0.0', port=8123, debug=True)
