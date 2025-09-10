async function get_genres_graphic() {
    response = await fetch("/get", {
        "method":"POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": JSON.stringify({
            "action":"get_genres"
        })
    })
    response = await response.json()
    genres = Object.keys(response)
    values = Object.values(response)
    
    total_singers = 0

    percentages = []

    for (let i = 0; i < values.length ; i++)
    {
        total_singers += values[i]
    }

    for (let i = 0; i < values.length ; i++)
    {
        percentage = (values[i] * 100) / total_singers
        percentages.push(percentage)
    }


    

    graphic_div = document.querySelector(".genres_graphic")
    colors = []
    
    for (let i = 0; i < genres.length; i++)
    {
        colors.push(chroma.random().hex())
    };

    
    new Chart(graphic_div, {
        "type":"bar",
        data: {
        labels: genres,
        datasets: [{
            label: 'Porcentagem', // legenda
            data: percentages,    // valores
            backgroundColor: colors // cores
        }] 
    }})
}

async function main() {
    await get_genres_graphic()
}


document.addEventListener("DOMContentLoaded", main)