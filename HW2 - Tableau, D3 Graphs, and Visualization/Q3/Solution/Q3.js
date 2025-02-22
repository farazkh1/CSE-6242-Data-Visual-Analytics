const games = ['Catan', 'Dominion', 'Codenames', 'Terraforming Mars', 'Gloomhaven', 'Magic: The Gathering', 'Dixit', 'Monopoly'];

// Declare global variables to store the transformed data so we can access it from console
var dates = [];
var gamestats = {
    count: {},
    rank: {}
};
var maxCount = 0;
var foobar; // for debugging

// Load data ------------------------------------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------------------------------------
d3.csv("boardgame_ratings.csv").then(function (data) {

    games.forEach(function (game) {
        gamestats.count[game] = [];
        gamestats.rank[game] = [];
    });

    // Iterate over each row in the data to extract dates, counts, and ranks
    data.forEach(function (d) {

        // Parse and store the date
        let date = d3.timeParse("%Y-%m-%d")(d.date);
        dates.push(date);

        // Store count and rank for each game
        games.forEach(function (game) {
            let game_count = +d[`${game}=count`]
            let game_rank = +d[`${game}=rank`]
            gamestats.count[game].push(game_count);
            gamestats.rank[game].push(game_rank);
            maxCount = Math.max(maxCount, game_count);
        });
    });

// Prep -----------------------------------------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------------------------------------
    
    var Prep = function(version) {
        // Define the margins
        const margin = { top: 50, right: 150, bottom: 60, left: 80 },
            width = 900,
            height = 500;

        // Define x-scale
        const x = d3.scaleTime()
            .domain(d3.extent(dates))
            .range([margin.left, width - margin.right]);

        let y;
        // Define y-scale
        y = d3.scaleLinear()
            .domain([0, maxCount])
            .range([height - margin.bottom, margin.top]);
        
        // Scale variation for c
        if (version == "c-1") {
            y = d3.scaleSqrt()
                        .domain([0, maxCount])
                        .range([height - margin.bottom, margin.top]);
        }

        if (version == "c-2") {
            y = d3.scaleLog()
                    .domain([1, maxCount])
                    .range([height - margin.bottom, margin.top]);
        }

        // get tickValues. Will be useful later.
        const tickValues = x.ticks(d3.timeMonth.every(3));
        const tickTimestamps = tickValues.map(date => date.getTime());
        const tickIndices = [];
        // get tickIndices for each value.
        for (const [index, date] of dates.entries()) {
            if (tickTimestamps.includes(date.getTime())) {
                tickIndices.push(index);
            }
        };
        console.log(y());        
        return {margin, width, height, x, y, tickValues, tickIndices};
    }

// Helper Functions ------------------------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------------------------------

    // Create a function to add the x-axis

    var Helper = function({margin, width, height, x, y, tickValues, tickIndices}) {

        const createSVG = function(version) {
            return d3.create("svg")
                .attr("id", "svg-" + version)
                .attr("width", width)
                .attr("height", height)
                .attr("viewBox", [0, 0, width, height]);
        };

        var xAxis = g => g
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x)
                .tickValues(tickValues) // Set custom tick values for every 3 months
                .tickFormat(d3.timeFormat("%b %y")));
            
        // Create a function to add the y-axis
        var yAxis = g => g
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y));

        var xAxisLabel = g => g
            .append("text")
            .attr("x", (width - margin.left - margin.right) / 2 + margin.left)
            .attr("y", height - margin.bottom + 40)
            .attr("class", "label")
            .text("Month");
        
        var yAxisLabel = g => g
            .append("text")
            .attr("x", -(height / 2))
            .attr("y", margin.left - 60)
            .attr("class", "label")
            .attr("transform", "rotate(-90)")
            .text("Num of Ratings");


        // Function to add chart title
        const addChartTitle = g => g
                .append("text")
                .attr("x", (width - margin.left - margin.right) / 2 + margin.left)
                .attr("y", margin.top / 2)
                .attr("class", "title")
                .text("Number of Ratings 2016-2020");

        // Define a color scale
        var color = d3.scaleOrdinal(d3.schemeCategory10)
                        .domain(games);
        
        // Function to plot lines
        plotLines = function(g) {
            games.forEach(game => {
                const line = d3.line()
                    .x((d, i) => x(dates[i]))
                    .y(d => y(d));

                g.append("path")
                    .datum(gamestats.count[game])
                    .attr("fill", "none")
                    .attr("stroke", color(game))
                    .attr("stroke-width", 2)
                    .attr("d", line);
                // add text description to each line
                g.append("text")
                    .attr("x", x(dates[dates.length - 1]) + 5) // Set x position slightly to the right of the last point
                    .attr("y", y(gamestats.count[game][dates.length - 1])) // Set y position based on the last count value
                    .text(game) // Use the game name as the label
                    .attr("class", "legend")
                    .attr("fill", color(game))
                    .attr("alignment-baseline", "middle"); // Set the text color to match the line color
            })
        }

        plotRank = function(g, trackedGames) {

            // get filtered data first
            trackedGames.forEach(game => {
                const filteredData = tickIndices.map(index => ({
                    date: dates[index],
                    rank: gamestats.rank[game][index],
                    count: gamestats.count[game][index]
                }));

            // Append circles for the filtered data
            g.append("g")
                .selectAll("circle")
                .data(filteredData)
                .enter()
                .append("circle")
                .attr("cx", d => x(d.date)) // Position x based on the filtered date
                .attr("cy", d => y(d.count)) // Position y based on the filtered ranking
                .attr("class", "rankSymbol")
                .attr("r", 10)
                .attr("fill", color(game));

            g.append("g")
                .selectAll("text")
                .data(filteredData)
                .enter()
                .append("text")
                .attr("x", d => x(d.date))
                .attr("y", d => y(d.count) + 4)
                .text(d => d.rank) // Set the text content as the rank
                .attr("class", "rank")
            });
        }

        addLegend = function(g) {
            const legendX = width - margin.right + 60;
            const legendY = height - margin.bottom - 30;

            // Append a group for the legend
            const legend = g.append("g")
                .attr("class", "legend")
                .attr("transform", `translate(${legendX}, ${legendY})`);

            // Append a circle to represent the legend symbol
            legend.append("circle")
                .attr("cx", 0)
                .attr("cy", 0)
                .attr("r", 10)
                .attr("fill", "black");
            
            legend.append("text")
                .attr("y", 2)
                .attr("class", "rank")
                .text("Rank");

            // Append text below the circle for the description
            legend.append("text")
                .attr("x", 0)
                .attr("y", 20) // Position below the circle
                .attr("text-anchor", "middle") // Center align the text with the circle
                .style("font-size", "10px")
                .text("BoardGameGeek Rank");
            
        }
        return {createSVG, xAxis, yAxis, xAxisLabel, yAxisLabel, addChartTitle, color, plotLines, plotRank, addLegend};
    }

    // Begins!! -------------------------------------------------------------------------------------------------------------------------------
    // Actual chart building -------------------------------------------------------------------------------------------------------------------------
    // Create a function to generate the first chart
    const chart = function(version) {

        const {createSVG, xAxis, yAxis, xAxisLabel, 
        yAxisLabel, addChartTitle, color, plotLines, 
        plotRank, addLegend} = Helper(Prep(version));

        // Create an SVG element
        const svg = createSVG(version);
    
        // Add chart title
        title = svg.append("g")
                    .attr("id", "title-"+version)
                    .call(addChartTitle);

        const title_addition = {
            "a": "",
            "b": " with Rankings",
            "c-1": " (Square root Scale)",
            "c-2": " (Log Scale)"
        };

        svg.select("#title-" + version).select("text")
            .text(function() {
                return d3.select(this).text() + title_addition[version];
            });
            

        // add overarching plot element
        plot = svg.append("g")
                .attr("id", "plot-"+version);
        
        // add plot lines
        lines = plot.append("g")
                    .attr("id", "lines-"+version)
                    .call(plotLines);
        
        // Append a group for the x-axis and call the xAxis function
        xAxisPlot = plot.append("g")
                        .attr("id", "x-axis-"+version)
                        .call(xAxis)
                        .call(xAxisLabel);
    
        // Append a group for the y-axis and call the yAxis function
        yAxisPlot = plot.append("g")
                        .attr("id", "y-axis-"+version)
                        .call(yAxis)
                        .call(yAxisLabel);
        
        // moving beyond the first graph
        if (version != "a") {
            // Add circles only for the filtered tick dates for specific tracked games
            const trackedGames = ['Catan', 'Codenames', 'Terraforming Mars', 'Gloomhaven'];
            symbols = plot.append("g")
                            .attr("id", "symbols-"+version)
                            .call(g => plotRank(g, trackedGames));

            legend = svg.append("g")
                        .attr("id", "legend-"+version)
                        .call(addLegend);
        }

        // Return the SVG node so it can be appended to the DOM
        return svg.node();
    };


    // Append the SVG to the body of the document to display the chart
    document.body.append(chart("a"));
    document.body.append(chart("b"));
    document.body.append(chart("c-1"));
    document.body.append(chart("c-2"));

    const signatureDiv = document.createElement('div');
    signatureDiv.id = 'signature';
    signatureDiv.textContent = 'your GT Username'; // Add you GT username here

    // Add styles directly for positioning if needed
    signatureDiv.style.position = 'fixed';
    signatureDiv.style.bottom = '0';
    signatureDiv.style.right = '0'; // This ensures it's at the bottom-right corner
    signatureDiv.style.backgroundColor = 'white';
    signatureDiv.style.padding = '10px';
    signatureDiv.style.zIndex = '9999';

    // Append the div to the end of the body
    document.body.appendChild(signatureDiv);
});