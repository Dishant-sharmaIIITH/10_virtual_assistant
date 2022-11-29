
const json_path = './data.json';
var curr_idx = 0;
function promptSnippet(snippet) {

    // alert(snippet);

    document.getElementById('snippet').value = snippet;
    document.getElementById('snippet').style.display = 'block';
    document.getElementById('snippet').style.position = 'absolute';
    document.getElementById('snippet').style.top = '50%';
    document.getElementById('snippet').style.left = '50%';
    setTimeout(() => {
        document.getElementById('snippet').style.display = 'none';
    }
        , 5000);


}



async function printJson() {
    const response = await fetch(json_path);
    const data = await response.json();
    console.log(data);


    console.log(data);
    const table = document.getElementById('json_table');

    for (let i = 0; i < data.length; i++) {
        const row = `<tr>
        <td>${data[i].Sender}</td>
        <td><a href="#" onclick="promptSnippet('${data[i].Snippet}')">${data[i].Subject}</a></td>
        <td>${data[i].Date}</td>
        </tr>`;
        table.innerHTML += row;
        curr_idx = i;

    }


}

printJson();