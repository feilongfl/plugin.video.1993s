
function decode(url) {
    let urlList = url.split('').reverse()
    let result = ""

    for (let i = 0; i < urlList.length; i += 2) {
        let a = parseInt(urlList[i] + urlList[i + 1], 16);
        result += String.fromCharCode(a)
    }

    i = 0
    do {
        i = result.indexOf(Date.now().toString().substr(0, 4), i + 1)
        fake = parseInt(result.substr(i, 6) + "0000000")
        // console.log(i, fake, Date.now(), fake > Date.now())
    } while (fake > Date.now())
    result.replace(result.substr(i, 6), "", 1)
    // console.log(result)
    return result
}

console.log(decode(process.argv[process.argv.length - 1]))
