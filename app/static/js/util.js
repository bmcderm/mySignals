var API_ROUTE = '/api/v1';

class ColorCategory {
    static get Primary() {
        return 'primary';
    }
    static get Success() {
        return 'success';
    }
    static get Danger() {
        return 'danger';
    }
    static get Info() {
        return 'info';
    }
    static get Secondary() {
        return 'secondary';
    }
    static get Warning() {
        return 'warning';
    }
    static get Light() {
        return 'light';
    }
    static get Dark() {
        return 'dark';
    }
}

function newAlert(message, category = ColorCategory.Primary, parentID = 'alertParent', replace = true) {
    let s = `
        <div class="alert alert-${category} alert-dismissible fade show" role="alert">
            ${message}
            
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">×</span>
            </button>
        </div>
    `;

    if (replace) $(`#${parentID}`).html(s);
    else $(`#${parentID}`).append(s);
}

function isEmailValid(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function containsSpecialCharacters(str) {
    return !(!/[~`!#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?]/g.test(str));
}
