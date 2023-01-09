var state_select = document.getElementById('state')
var city_select = document.getElementById('city')
var hospital_select = document.getElementById('hospital')
var insurance_select = document.getElementById('insurance')
state_select.addEventListener("change", update_cities)
function update_cities() {
    state = state_select.value;
    fetch('/cities/' + state).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '';
            for (var cit of data.cities) {
                optionHTML += '<option value="' + cit.toUpperCase() + '">' + cit + '</option>';
                };
            city_select.innerHTML = optionHTML;
            update_hospitals()
            });
        });
    }
city_select.addEventListener("change", update_hospitals)
function update_hospitals() {
    city = city_select.value;
    state = state_select.value;
    fetch('/hospitals/' + city + '/' + state).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '';
            for (var hos of data.hospitals) {
                optionHTML += '<option value="' + hos.toUpperCase() + '">' + hos + '</option>';
                };
            hospital_select.innerHTML = optionHTML;
            update_insurances()
            });
        });
    }
hospital_select.addEventListener("change", update_insurances)
function update_insurances() {
    chosen_hospital = hospital_select.value;
    fetch('/insurances/' + chosen_hospital).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '';
            for (var ins of data.insurances) {
                optionHTML += '<option value="' + ins.toUpperCase() + '">' + ins + '</option>';
                console.log(ins)
                };
            insurance_select.innerHTML = optionHTML;
            });
        });
    }