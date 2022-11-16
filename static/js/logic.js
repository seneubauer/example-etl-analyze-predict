/* ----- global declarations ----- */

// html elements
let available_drawings = d3.select("#available_drawings");
let associated_revisions = d3.select("#associated_revisions");
let associated_items = d3.select("#associated_items");

// initialize the page
init();

/* ----- initializer ----- */
function init()
{
    // assign events
    available_drawings.on("change", Get_Associated_Unique_Revisions)
    available_drawings.on("change", Get_Associated_Unique_Items)

    Get_All_Unique_Drawings();
}

/* ----- routes ----- */

// query the database for characteristic data
function Get_Part_Characteristics()
{
    // retrieve the current selected parameters
    let drawing = available_drawings.property("value");
    let revision = associated_revisions.property("value");
    let item = associated_items.property("value");

    // call the flask server
    d3.json(`get_characteristics/${drawing}/${revision}/${item}/`).then(function (data)
    {
        
    });
}

// populate the select control with a list of unique drawing numbers
function Get_All_Unique_Drawings()
{
    // call the flask server
    d3.json("get_all_unique_drawings/").then(function (data)
    {
        if (data.status == "ok")
        {
            available_drawings.selectAll("option").data(data.response).enter().append("option").text(x => x).attr("value", x => x);
        }
        else
        {
            console.log(data.response);
        }
        
        Get_Associated_Unique_Revisions();
        Get_Associated_Unique_Items();
    });
}

// populate the select control with a list of unique associated revisions
function Get_Associated_Unique_Revisions()
{
    // retrieve the current selected drawing
    let drawing = available_drawings.property("value");

    // call the flask server
    d3.json(`get_associated_unique_revisions/${drawing}/`).then(function (data)
    {
        if (data.status == "ok")
        {
            associated_revisions.selectAll("option").remove();
            associated_revisions.selectAll("option").data(data.response).enter().append("option").text(x => x).attr("value", x => x);
        }
        else
        {
            console.log(data.response);
        }
    });
}

// populate the select control with a list of unique associated items
function Get_Associated_Unique_Items()
{
    // retrieve the current selected drawing
    let drawing = available_drawings.property("value");

    // call the flask server
    d3.json(`get_associated_unique_items/${drawing}/`).then(function (data)
    {
        if (data.status == "ok")
        {
            associated_items.selectAll("option").remove();
            associated_items.selectAll("option").data(data.response).enter().append("option").text(x => x).attr("value", x => x);
        }
        else
        {
            console.log(data.response);
        }
    });
}