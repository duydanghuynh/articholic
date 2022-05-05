var editArticleId = null;

window.onload = function () {    
    loadTheArticles();
};
//=============================================================
function loadTheArticles(){    
    refreshInfo();
    var addButton =document.querySelector("#add-button");
    var editButton = document.querySelector("#edit-button");
    editButton.style.display="none";
    var submitButton = document.querySelector("#submit-button");
    submitButton.style.display="none";
    var cancelButton = document.querySelector("#cancel-button");
    cancelButton.style.display="none";
    fetch("http://localhost:8080/articles",{        
        credentials:"include"
    }).then(function (response) {
        // console.log(response.status);
        if (response.status==200){
            console.log("loadTheArticles is loaded");
            //TODO: logged in!!!!
            //show articles
            //decode Json data from response:
            hideLogin();
            showArticles();
            addButton.style.display="block";
            response.json().then(function (data) {//then is a promise
                //save and/or use the data
                //data is an array of cookies                
                articles = data;
                console.log("Articles are loaded from server:", articles);
                //1.query PARENT element
                var articleItems = document.querySelector("#items");
                articleItems.innerHTML=""; 
                data.forEach(function(article){
                //2. create new child
                    var item = document.createElement("li");
                    item.setAttribute("class","article-item");
                    item.innerHTML += article.title;
                    //=====delete button===============             
                    var deleteButton = document.createElement("button");
                    deleteButton.innerHTML="X"
                    deleteButton.setAttribute("class","delete-btn");
                    deleteButton.onclick=function(){
                        // deleteArticleFromServer(cookies.id);
                        //new stuff!!!
                        if(confirm("Are you sure you want to delete "+article.title+" ?")){
                            deleteArticleFromServer(article.id);
                        }
                    }
                    item.appendChild(deleteButton);
                    //==================================
                    item.onclick=function(){
                        getAnArticleFromServer(article.id);
                    }               
                    articleItems.appendChild(item);
                })
            });
        }else{ //if(response.status==401){
            //TODO:hide article--frame:
            hideArticles();
            addButton.style.display="none";
            return
        }
    });
}
//============================================================
function insertNewArticle(title,author,code,content){
    var data ="title="+ encodeURIComponent(title)+"&author="+ encodeURIComponent(author)+"&code="+ encodeURIComponent(code)+"&content="+ encodeURIComponent(content); //encodeURIComponent
    fetch("http://localhost:8080/articles",{
        //Method:
        method:"POST",
        //Headers
        headers:{
            "Content-Type":"application/x-www-form-urlencoded"
        },
        //body
        body: data,
        credentials:"include"
    }).then(function(response){
        console.log("insertNewArticle worked! Reload the list of articles");
        loadTheArticles();
    });
}
//===================================================================
function deleteArticleFromServer(id){
    fetch("http://localhost:8080/articles/"+id,{
        //Method:
        method:"DELETE",
        credentials:"include"
    }).then(function(response){
        console.log("deleteArticleFromServer worked! Reload the list of articles");
        loadTheArticles();
    });
}
//===================================================================
function updateArticleFromServer(title,author,code,content,id){
    var data ="title="
    + encodeURIComponent(title)+"&author="
    + encodeURIComponent(author)+"&code="
    + encodeURIComponent(code)+"&content="
    + encodeURIComponent(content);
    fetch("http://localhost:8080/articles/"+id,{
        //Method:
        method:"PUT",
        //Headers
        headers:{
            "Content-Type":"application/x-www-form-urlencoded"
        },
        //body
        body: data,
        credentials:"include"
    }).then(function(resonse){
        console.log("updateArticleFromServer worked! Reload the list of articles");
        loadTheArticles();
    });
}
//===================================================================
function getAnArticleFromServer(id){
    fetch("http://localhost:8080/articles/"+id,{
        //Method:
        method:"GET",
        credentials:"include"
    }).then(function(response){
        response.json().then(function (data){
            console.log(data);console.log("getAnArticleFromServer worked!");

            var editButton = document.querySelector("#edit-button");
            var submitButton = document.querySelector("#submit-button");
            var cancelButton = document.querySelector("#cancel-button");

            title_input = document.querySelector("#title");
            title_input.value=data.title;
            title_input.disable=true;
            author_input = document.querySelector("#author");
            author_input.value=data.author;
            author_input.disable=true;
            code_input = document.querySelector("#code");
            code_input.value=data.code;
            code_input.disable=true;
            content_input = document.querySelector("#content");
            content_input.value=data.content;
            content_input.disable=true;                    
            editButton.style.display="block";                   
            cancelButton.style.display="none";                   
            submitButton.style.display="none";
            //======================
            editButton.onclick=function(){
                title_input.disable=false;
                author_input.disable=false;
                code_input.disable=false;
                content_input.disable=false;
    
                editArticleId = data.id;
                editButton.style.display="none";
                submitButton.style.display="block";                
                cancelButton.style.display="block"; 
                submitButton.onclick=function(){
                    //todo: comeback for this
                    updateArticleFromServer(title_input.value,author_input.value,code_input.value,content_input.value,editArticleId);
                }
            }
        });
    });
}
//===================================================================
function refreshInfo(){
    title_input = document.querySelector("#title");
    title_input.value="";
    title_input.disabled=true;
    author_input = document.querySelector("#author");
    author_input.value="";
    author_input.disabled=true;
    code_input = document.querySelector("#code");
    code_input.value="";
    code_input.disabled=true;
    content_input = document.querySelector("#content");
    content_input.value="";
    content_input.disabled=true;
}
//===================================================================
function clearInfo(){
    editArticleId = null;
    title_input = document.querySelector("#title");
    title_input.value="";
    title_input.disable=false;
    author_input = document.querySelector("#author");
    author_input.value="";
    author_input.disable=false;
    code_input = document.querySelector("#code");
    code_input.value="";
    code_input.disable=false;
    content_input = document.querySelector("#content");
    content_input.value="";
    content_input.disable=false;
    var editButton = document.querySelector("#edit-button");
    editButton.style.display="none";
    
}//===================================================================
function cancelInfo(){
    clearInfo()
    var submitButton = document.querySelector("#submit-button");
    submitButton.style.display="none";
    var cancelButton = document.querySelector("#cancel-button");
    cancelButton.style.display="none";
}
//===================================================================
function blockModify(){
    title_input = document.querySelector("#title");
    title_input.disable=true;
    author_input = document.querySelector("#author");
    author_input.disable=true;
    code_input = document.querySelector("#code");
    code_input.disable=true;
    content_input = document.querySelector("#content");
    content_input.disable=true;
}
//====================================================================
var addButton = document.querySelector("#add-button"); 
addButton.onclick=function(){
    clearInfo();
    var submitButton = document.querySelector("#submit-button");
    var cancelButton = document.querySelector("#cancel-button");
    var title = document.querySelector("#title"); 
    var author = document.querySelector("#author"); 
    var code = document.querySelector("#code"); 
    var content = document.querySelector("#content"); 
    submitButton.style.display="block";
    cancelButton.style.display="block";
    submitButton.onclick=function(){
        //todo: comeback for this        
        var title_info = title.value
        var author_info = author.value
        var code_info = code.value
        var content_info = content.value
        insertNewArticle(title_info,author_info,code_info,content_info);
    }
}
//=======================================================================
//=======================================================================

function RegisterNewUser(usn,pwd,fname,lname){
    var data = "username="+ encodeURIComponent(usn)+"&password="+ encodeURIComponent(pwd)
    +"&firstname="+ encodeURIComponent(fname)+"&lastname="+ encodeURIComponent(lname); //encodeURIComponent
    fetch("http://localhost:8080/users",{
        //Method:
        method:"POST",
        //Headers
        headers:{
            "Content-Type":"application/x-www-form-urlencoded"
        },
        //body
        body: data,
        credentials:"include"// remember this to have credential!!!! cookies, sessions
    }).then(function(response){
        if(response.status==201){
            console.log("registernewuser worked!");
            hideRegisterForm();
            document.getElementById("register-alert1").style.display = "none";
            document.getElementById("register-alert2").style.display = "block";
        }else if(response.status==422){
            // TODO: show some error message, register failed(dup email)
            document.getElementById("register-alert1").style.display = "block";
        }
    });
}

function Login(usn,pwd){
    var data ="username="+ encodeURIComponent(usn)+"&password="+ encodeURIComponent(pwd)
    fetch("http://localhost:8080/sessions",{
        //Method:
        method:"POST",
        //Headers
        headers:{
            "Content-Type":"application/x-www-form-urlencoded"
        },
        //body
        body: data,
        credentials:"include"
    }).then(function(response){
        if(response.status==201){
            console.log("Login worked!");
            document.querySelector("#login-alert").innerHTML="Hi!"
            loadTheArticles();
            hideLogin();
        }else if(response.status==401){
            document.querySelector("#login-alert").style.display = "block";
        }
    });
}
//=================================================================

var registerFormButton = document.querySelector("#register-form-button");
var cancelRegisterButton = document.querySelector("#cancel-reg-button");
function openRegisterForm() {
    document.querySelector("#register-form").style.display = "block";
}  
function hideRegisterForm() {
    document.querySelector("#register-form").style.display = "none"; 
    document.querySelector("#firstname").value="";
    document.querySelector("#lastname").value="";
    document.querySelector("#username").value="";
    document.querySelector("#password").value="";
}
function showArticles(){    
    document.querySelector("#articles-frame").style.display="block";
}
function hideArticles(){    
    document.querySelector("#articles-frame").style.display="none";
}
function showLogin(){    
    document.querySelector("#login-form").style.display="block";
}
function hideLogin(){    
    document.querySelector("#login-form").style.display="none";
}

registerFormButton.onclick=function(){
    openRegisterForm();
    // registerFormButton.style.display="none";
    registerFormButton.style.disabled=true;
}
cancelRegisterButton.onclick=function(){
    hideRegisterForm();
    registerFormButton.style.display="block";
    registerFormButton.style.disabled=false;
}
//=================================================================
var registerButton = document.querySelector("#register-button");
registerButton.onclick=function(){
    // clearInfo();
    var username = document.querySelector("#username");
    var password = document.querySelector("#password");
    var firstname = document.querySelector("#firstname");
    var lastname = document.querySelector("#lastname");
    var usn = username.value
    var pwd = password.value
    var fname = firstname.value
    var lname = lastname.value
    RegisterNewUser(usn,pwd,fname,lname);
}
//==================================================================
var loginButton = document.querySelector("#login-button");
loginButton.onclick=function(){
    clearInfo();
    var username = document.querySelector("#li-username"); 
    var password = document.querySelector("#li-password"); 
    
    //todo: comeback for this        
    var usn = username.value
    var pwd = password.value
    Login(usn,pwd);
}
