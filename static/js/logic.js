/* ----- global declarations ----- */

// html elements
let characteristic_table = d3.select("#characteristic_table");
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
    d3.select("#retrieve_characteristics").on("click", Get_Part_Characteristics);

    d3.select("#data_requests_form").on("click", Open_Data_Requests);
    d3.select("#data_entry_form").on("click", Open_Data_Entry);
    d3.select("#exploratory_analysis_form").on("click", Open_Exploratory_Analysis);
    d3.select("#model_predictions_form").on("click", Open_Model_Predictions);
    d3.select("#model_parameters_form").on("click", Open_Model_Parameters);

    Get_All_Unique_Drawings();
}

/* ----- pages ----- */

// open the data requests page
function Open_Data_Requests()
{
    d3.json("data_requests").then(function (data)
    {
        console.log("Opened Data Requests");
    });
}

// open the data entry page
function Open_Data_Entry()
{
    d3.json("data_entry/").then(function (data)
    {
        console.log("Opened Data Entry");
    });
}

// open the exploratory analysis page
function Open_Exploratory_Analysis()
{
    d3.json("exploratory_analysis/").then(function (data)
    {
        console.log("Opened Exploratory Analysis");
    });
}

// open the model predictions page
function Open_Model_Predictions()
{
    d3.json("model_predictions/").then(function (data)
    {
        console.log("Opened Model Predictions");
    });
}

// open the model parameters page
function Open_Model_Parameters()
{
    d3.json("model_parameters/").then(function (data)
    {
        console.log("Opened Model Parameters");
    });
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
        if (data.status == "ok")
        {
            // create the table body
            let tbody = characteristic_table.select("tbody")

            // create the table rows
            tbody.selectAll("tr").remove();
            let rows = tbody.selectAll("tr")
                .data(data.response)
                .enter()
                .append("tr");
            
            // create the cells
            rows.selectAll("td")
                .data(x => [
                    x.index,
                    x.name,
                    x.nominal,
                    x.usl,
                    x.lsl,
                    x.part_drawing,
                    x.part_revision,
                    x.part_item,
                    x.unit_name,
                    x.characteristic_name,
                    x.is_gdt,
                    x.gauge,
                    x.gauge_type])
                    .enter()
                    .append("td")
                    .text(x => x);
        }
        else
        {
            console.log(data.response);
        }
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
            available_drawings.selectAll("option")
                .data(data.response)
                .enter()
                .append("option")
                .text(x => x)
                .attr("value", x => x);
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
            associated_revisions.selectAll("option")
                .data(data.response)
                .enter()
                .append("option")
                .text(x => x)
                .attr("value", x => x);
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
            associated_items.selectAll("option")
                .data(data.response)
                .enter()
                .append("option")
                .text(x => x)
                .attr("value", x => x);
        }
        else
        {
            console.log(data.response);
        }
    });
}