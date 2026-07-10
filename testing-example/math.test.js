const {addieren, subtrahieren, multiplizieren, dividieren} = require("./math")

test("addieren von 2 und 3 soll 5 sein", () => {
    expect(addieren(2,3)).toBe(5)
})

test("addieren von 5 und 10 soll nicht 7 ergeben" , () => {
    expect(addieren(5,10)).not.toBe(7)
})

test("subtrahieren von 2 und 3 soll -1 sein", () => {
    expect(subtrahieren(2,3)).toBe(-1)
})

test("multiplizieren von 2 und 3 soll 6 sein", () => {
    expect(multiplizieren(2,3)).toBe(6)
})

test("dividieren von 10 und 2 soll 5 sein", () => {
    expect(dividieren(10,2)).toBe(5)
})

test("dividieren von 10 und 0 soll einen Fehler auswerfen", () => {
    expect(() => dividieren(10,0)).toThrow("Division durch 0 ist nicht erlaubt!!!!!")
})
