/*
 *
 *
 * VARIABLES
 *
 *
 *
 */

var signals = [];
var allSignals;

/*
 *
 *
 * JQUERY
 *
 *
 *
 */

$(document).ready(function () {
    // Initialization
    allSignals = $('#allSignals');

    // Event listeners

    // Other
    getAllSignals();
});

/*
 *
 *
 * FUNCTIONS
 *
 *
 *
 */

function getAllSignals()
{
    let cardsHTML = '';

    $.get('/getRecentSignals', function (data)
    {
        // Get all the signals from the JSON
        signals = data.signals;

        for (let i = 0; i < data.signals.length; i++)
        {
            // Add a single card to the html string
            cardsHTML += `
                <div class="row justify-content-center mb-5">
                    <div class="col-6 col-xl-4 col-lg-6 col-md-8 col-sm-10 d-flex">
                        <div class="card h-100 bg-dark rounded-lg">
                            <a class="card-body my-auto" href="#!">
                                <h3 class="mt-auto font-weight-bold text-white">
                                    It's the little touches that make memories.
                                </h3>
    
                                <p class="mb-0 text-muted">
                                    ${data.signals[i].cryptoType}
                                </p>
                            </a>
    
                            <a class="card-meta" href="#!">
                                <!-- Divider -->
                                <hr class="card-meta-divider">
    
                                <div class="avatar avatar-sm mr-2">
                                    <img src="https://pbs.twimg.com/profile_images/1292159368943693824/JXYCQur0_400x400.jpg"
                                        class="avatar-img rounded-circle">
                                </div>
    
                                <h6 class="text-uppercase text-muted mr-2 mb-0">
                                    Bitcoin
                                </h6>
    
                                <p class="h6 text-uppercase text-muted mb-0 ml-auto">
                                    <time datetime="2019-05-02">Today</time>
                                </p>
                            </a>
                        </div>
                    </div>
                </div>
            `;
        }

        allSignals.html(cardsHTML);
    });
}
