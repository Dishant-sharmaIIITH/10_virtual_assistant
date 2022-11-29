
console.log("hello dashboard")
var word="Cricket";

var obox = document.getElementById("outerbox");



obox.innerHTML="";

function getdata() {
    // fetchads(); 
      obox.innerHTML="";
      url = "https://gnews.io/api/v4/search?q="+word+"&token=6aaf3bfcab86588ed47a0d6c96ffc752"
      fetch(url).then((response) => {
          console.log("fetch");
          return response.json();
      }).then((data) => {
          console.log(data)
          let array = data.articles;
         // nimg.src = array[0].image;
          //var obj=JSON.parse(data.articles[0]);
          // console.log(obj.title);
          // let adsres;
  
          // fetch("data.json")
          // .then(response => response.json())
          // .then(json => adsres=json)
          // .then(()=>console.log(adsres));
              
  
  
          //console.log(adsres);
          for (i = 0; i < array.length; i++) {
  
            // if(i>0&&i%3==0){
              
  
  
            //     x=i/3;
            //     console.log(x);
  
            //     // const firstimg=document.getElementById("firstimg");
            //   var adsdiv = `<div class="row g-0 justify-content-center">
                    
            //   <img src="${adsres[x].src}" style="height: 200px; width:600px">
              
            //   </div>`;
  
            //   obox.innerHTML+=adsdiv;
  
              
              
  
            // }
  
  
  
  
      var innerdiv = `<div class="card1" id="idiv">
            <div class="row g-0">
              <div class="col-md-4">
                <img src="${array[i].image}"class="img-fluid rounded-start" id="newsimg" alt="...">
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title" id="ntitle">${array[i].title}</h5>
                  <p class="card-text" id="ntext">${array[i].description}</p>
                  <p class="card-text"><small class="text-muted">${array[i].publishedAt}
                  </small></p>
              <a href="${array[i].url}" class="btn btn-secondary">Read More</a>
              <p>____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________</p>
                </div>
              </div>
            </div>
          </div>
          <br>`;
          obox.innerHTML+=innerdiv;
  
          }
          //obox.appendChild()
      });
  }

  // getdata();

  fetch('/topicOfInterest')
  .then(function (response) {
    return response.json();
  }).then(function (text) {
    console.log('GET response:');
    console.log(text.TOI);
    word='Cricket'
    word=text.TOI;
    if(word==''){
      word='cricket'
    }
    getdata();
    
  });

  fetch('/login_valid')
      .then(function (response) {
        return response.json();
      }).then(function (text) {
        console.log('GET response:');
        console.log(text.greeting);
        console.log(text.email);
      });