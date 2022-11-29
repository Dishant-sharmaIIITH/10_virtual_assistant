const DisplayTodoList=()=>{
    let All_item_notes = localStorage.getItem("All_item_notes");
    if (!All_item_notes) notes = [];
    else notes = JSON.parse(All_item_notes);
    let html = "";
    for(let index=0;index<notes.length;index++) {
       html +=`
       <div style="display: flex; grid-gap: 18px;">
             <p class="card-text">${notes[index]}</p>
             <i id="${index}" style="cursor:pointer; color: red; fontsize: 20px" onclick=
             "DelNoteItem(this.id)" class="fa fa-trash"></i>
       </div>
       <br>
       <br>
       `;
    }
    let localStorage_Notes = document.getElementById("All_item_notes");
    if (notes.length == 0)
       localStorage_Notes.innerHTML = `🙄 No notes for now..`;
    else
       localStorage_Notes.innerHTML = html;
 }
 document.getElementById("AddNotesBtn").addEventListener("click", ()=>{
    let todoText = document.getElementById("todoText");
    if(!(todoText.value)){
       alert("Please write something to create todo.")
       return;
    }
    let All_item_notes = localStorage.getItem("All_item_notes");
    if (!All_item_notes) NoteListObj = [];
    else
    NoteListObj = JSON.parse(All_item_notes);
    NoteListObj.push(todoText.value);
    localStorage.setItem("All_item_notes", JSON.stringify(NoteListObj));
    todoText.value = "";
    DisplayTodoList();
 });
 const DelNoteItem=(ind)=>{
    let All_item_notes = localStorage.getItem("All_item_notes");
    if (All_item_notes != null)
    notes = JSON.parse(All_item_notes);
    notes.splice(ind, 1);
    let str_notes=JSON.stringify(notes);
    localStorage.setItem("All_item_notes",str_notes);
    DisplayTodoList();
 }
 DisplayTodoList();