function maximizeToggle() {
    $('.card--input').toggleClass('card__maximized');
}
function dashboardToggle() {
    console.log('clicked');
    $('.dashboard--base').toggleClass('active');
}

// Shows the instruction modal
function instructionModalToggle () {
    $('.instruction-modal-overlay-back').toggleClass('show');
}
// instruction modal interactions
$('.instruction-modal-overlay-back').on('click', function(e) {
    if (e.target !== this)
        return;
    instructionModalToggle();
});
$('.instruction-modal-overlay-back button').on('click', function(e) {
    if (e.target !== this)
        return;
    instructionModalToggle();
});


$(document).ready(function(){
    var itemsToGrab = '';
    $('select').each(function(i, select){
        itemsToGrab += itemsToGrab.length > 0 ? ',' : '';
        itemsToGrab += select.name;
    });
    if(itemsToGrab.length > 0)
        $.get('/api/options/' + itemsToGrab, function(result){
            $.each(result, function(i, option){
                var option_html = '<option value=' + option.value + '>' + option.display_name + '</option>';
                $('select[name=' + option.field_name + ']').append(option_html);
            });
        });
});

var x, i, j, l, ll, selElmnt, a, b, c;
/* Look for any elements with the class "input__select": */
x = document.getElementsByClassName("input__select");
l = x.length;
for (i = 0; i < l; i++) {
    selElmnt = x[i].getElementsByTagName("select")[0];
    ll = selElmnt.length;
    /* For each element, create a new DIV that will act as the selected item: */
    a = document.createElement("DIV");
    a.setAttribute("class", "select-selected");
    a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
    x[i].appendChild(a);
    /* For each element, create a new DIV that will contain the option list: */
    b = document.createElement("DIV");
    b.setAttribute("class", "select-items select-hide");
    for (j = 1; j < ll; j++) {
        /* For each option in the original select element,
        create a new DIV that will act as an option item: */
        c = document.createElement("DIV");
        c.innerHTML = selElmnt.options[j].innerHTML;
        c.addEventListener("click", function(e) {
            /* When an item is clicked, update the original select box,
            and the selected item: */
            var y, i, k, s, h, sl, yl;
            s = this.parentNode.parentNode.getElementsByTagName("select")[0];
            sl = s.length;
            h = this.parentNode.previousSibling;
            for (i = 0; i < sl; i++) {
                if (s.options[i].innerHTML == this.innerHTML) {
                    s.selectedIndex = i;
                    h.innerHTML = this.innerHTML;
                    y = this.parentNode.getElementsByClassName("same-as-selected");
                    yl = y.length;
                    for (k = 0; k < yl; k++) {
                        y[k].removeAttribute("class");
                    }
                    this.setAttribute("class", "same-as-selected");
                    break;
                }
            }
            h.click();
        });
        b.appendChild(c);
    }
    x[i].appendChild(b);
    a.addEventListener("click", function(e) {
        /* When the select box is clicked, close any other select boxes,
        and open/close the current select box: */
        e.stopPropagation();
        closeAllSelect(this);
        this.nextSibling.classList.toggle("select-hide");
        this.classList.toggle("select-arrow-active");
    });
}
function closeAllSelect(elmnt) {
    /* A function that will close all select boxes in the document,
    except the current select box: */
    var x, y, i, xl, yl, arrNo = [];
    x = document.getElementsByClassName("select-items");
    y = document.getElementsByClassName("select-selected");
    xl = x.length;
    yl = y.length;
    for (i = 0; i < yl; i++) {
        if (elmnt == y[i]) {
            arrNo.push(i)
        } else {
            y[i].classList.remove("select-arrow-active");
        }
    }
    for (i = 0; i < xl; i++) {
        if (arrNo.indexOf(i)) {
            x[i].classList.add("select-hide");
        }
    }
}
/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect);


let options = document.getElementsByClassName("option");
for (i=0; i<options.length; i++){
    options[i].firstElementChild.addEventListener("click", function (e){
        if(this.parentNode.classList.contains("inactive")){
            this.parentNode.classList.remove("inactive")
        } else {
            this.parentNode.classList.add("inactive")
        }
    })
}


let singleHandedRangeSliders = document.getElementsByClassName("rangeSlider_singleHandled");
for (i=0; i<singleHandedRangeSliders.length; i++){
    initiateSingleHandedRangeSlider(singleHandedRangeSliders[i]);
}
function initiateSingleHandedRangeSlider(component) {
    let leftInput = component.children[0];
    let leftRange = component.children[1].children[1];

    leftRange.value = leftInput.value;
    leftRange.min = leftInput.min;
    leftRange.max = leftInput.max;
    leftRange.step = leftInput.step;

    leftInput.onchange = function (){
        var slider = this.parentNode.children[1].children[1];
        slider.value = this.value;
        var value=(100/(parseInt(slider.max)-parseInt(slider.min)))*parseInt(slider.value)-(100/(parseInt(slider.max)-parseInt(slider.min)))*parseInt(slider.min);
        var children = slider.parentNode.children[0].children;
        children[0].style.width=value+'%';
        children[1].style.width=100-value+'%';
        children[2].style.left=value+'%';
        children[3].style.left=value+'%';
        children[3].children[0].innerHTML=slider.value;
        slider.parentNode.parentNode.children[0].value=slider.value;
    };
    leftRange.oninput = function (){
        var value=(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.value)-(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.min);
        var children = this.parentNode.children[0].children;
        children[0].style.width=value+'%';
        children[1].style.width=100-value+'%';
        children[2].style.left=value+'%';
        children[3].style.left=value+'%';
        children[3].children[0].innerHTML=this.value;
        this.parentNode.parentNode.children[0].value=this.value;
    };
    leftRange.oninput();
}


let doubleHandedRangeSliders = document.getElementsByClassName("rangeSlider_doubleHandled");
for (i=0; i<doubleHandedRangeSliders.length; i++){
    initiateDoubleHandedRangeSlider(doubleHandedRangeSliders[i]);
}
function initiateDoubleHandedRangeSlider(component) {

    let leftInput = component.children[0];
    let leftRange = component.children[1].children[1];
    let rightRange = component.children[1].children[2];
    let rightInput = component.children[2];

    leftInput.onchange = function (){
        var slider = this.parentNode.children[1].children[1];
        slider.value = this.value;
        slider.value = Math.min(slider.value,slider.parentNode.children[2].value-(slider.value,slider.parentNode.children[2].step));
        var value=(100/(parseInt(slider.max)-parseInt(slider.min)))*parseInt(slider.value)-(100/(parseInt(slider.max)-parseInt(slider.min)))*parseInt(slider.min);
        var children = slider.parentNode.children[0].children;
        children[0].style.width=value+'%';
        children[2].style.left=value+'%';
        children[3].style.left=value+'%';children[5].style.left=value+'%';
        children[5].children[0].innerHTML=slider.value;
        slider.parentNode.parentNode.children[0].value=slider.value;
    };
    leftRange.oninput = function (){
        this.value = Math.min(this.value,this.parentNode.children[2].value-(this.value,this.parentNode.children[2].step));
        var value = (100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.value)-(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.min);
        var children = this.parentNode.children[0].children;
        children[0].style.width=value+'%';
        children[2].style.left=value+'%';
        children[3].style.left=value+'%';children[5].style.left=value+'%';
        children[5].children[0].innerHTML=this.value;
        this.parentNode.parentNode.children[0].value=this.value;
    };

    leftRange.value = leftInput.value;
    leftRange.min = leftInput.min;
    leftRange.max = leftInput.max;
    leftRange.step = leftInput.step;

    leftRange.oninput();

    rightRange.oninput = function (){
        this.value=Math.max(this.value,this.parentNode.children[1].value-(-(this.value,this.parentNode.children[1].step)));
        var value=(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.value)-(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.min);
        var children = this.parentNode.children[0].children;
        children[1].style.width=(100-value)+'%';
        children[2].style.right=(100-value)+'%';
        children[4].style.left=value+'%';children[6].style.left=value+'%';
        children[6].children[0].innerHTML=this.value;
        this.parentNode.parentNode.children[2].value=this.value;
    };
    rightInput.onchange = function (){
        var slider = this.parentNode.children[1].children[2];
        slider.value = this.value;
        slider.value=Math.max(slider.value,slider.parentNode.children[1].value-(-(slider.value,slider.parentNode.children[1].step)));
        var value=(100/(parseInt(slider.max)-parseInt(slider.min)))*parseInt(slider.value)-(100/(parseInt(slider.max)-parseInt(slider.min)))*parseInt(slider.min);
        var children = this.parentNode.children[0].children;
        children[1].style.width=(100-value)+'%';
        children[2].style.right=(100-value)+'%';
        children[4].style.left=value+'%';children[6].style.left=value+'%';
        children[6].children[0].innerHTML=slider.value;
        slider.parentNode.parentNode.children[2].value=slider.value;
    };

    rightInput.min = leftInput.min;
    rightInput.max = leftInput.max;
    rightInput.step = leftInput.step;

    rightRange.value = rightInput.value;
    rightRange.min = rightInput.min;
    rightRange.max = rightInput.max;
    rightRange.step = rightInput.step;

    rightRange.oninput();
}


let units = document.getElementsByClassName("unit__select");
for (i=0; i<units.length; i++){
    initiateUnitSelect(units[i]);
}
function initiateUnitSelect(component) {

    let unitSelect = component.children[0];
    let unitOptions = unitSelect.children;
    let selectedOptionIndex = unitSelect.selectedIndex===-1 ? 0 : unitSelect.selectedIndex;
    if (unitOptions.length === 1){
        // Adding span for unit
        component.innerHTML +=
            '                                        </span>\n' +
            '                                        <span class="units">\n' +
            '                                        </span>\n'

        let unitsSpans="";
        unitsSpans += "<span value="+ '"' +unitOptions[0].value+ '"' +">"+unitOptions[0].innerHTML+"</span>"

        component.children[1].innerHTML = unitsSpans;
        component.children[1].children[selectedOptionIndex].classList.add('show');
        // unitSelect.selectedIndex = selectedOptionIndex;
    } else {
        // Adding arrows and spans for units
        component.innerHTML += '                                        <span class="arrow arrow-up" onclick="unitArrowUp(this);">\n' +
            '                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="10.526" viewBox="0 0 16 10.526">\n' +
            '                                                        <g id="options-dropdown" data-name="Group 103" transform="translate(-1674 -182.929)">\n' +
            '                                                           <rect id="Rectangle_686" data-name="Rectangle 686" width="11.314" height="3.573" rx="1.786" transform="translate(1676.526 182.929) rotate(45)"/>\n' +
            '                                                           <rect id="Rectangle_687" data-name="Rectangle 687" width="11.314" height="3.573" rx="1.786" transform="translate(1690 185.456) rotate(135)"/>\n' +
            '                                                        </g>\n' +
            '                                            </svg>\n' +
            '                                        </span>\n' +
            '                                        <span class="units">\n' +
            '                                        </span>\n' +
            '                                        <span class="arrow arrow-down" onclick="unitArrowDown(this);">\n' +
            '                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="10.526" viewBox="0 0 16 10.526">\n' +
            '                                                        <g id="options-dropdown" data-name="Group 103" transform="translate(-1674 -182.929)">\n' +
            '                                                           <rect id="Rectangle_686" data-name="Rectangle 686" width="11.314" height="3.573" rx="1.786" transform="translate(1676.526 182.929) rotate(45)"/>\n' +
            '                                                           <rect id="Rectangle_687" data-name="Rectangle 687" width="11.314" height="3.573" rx="1.786" transform="translate(1690 185.456) rotate(135)"/>\n' +
            '                                                        </g>\n' +
            '                                            </svg>\n' +
            '                                        </span>'

        let unitsSpans="";
        for (j=0; j<unitOptions.length; j++){
            unitsSpans += "<span value="+ '"' +unitOptions[j].value+ '"' +">"+unitOptions[j].innerHTML+"</span>"
        }
        component.children[2].innerHTML = unitsSpans;
        component.children[2].children[selectedOptionIndex].classList.add('show');
        // unitSelect.selectedIndex = selectedOptionIndex;
    }

}
function unitArrowUp(elmnt){
    let units = elmnt.parentNode.children[2].children;
    let length = units.length;
    let select = elmnt.parentNode.children[0];
    for (i=0; i<length; i++){
        if (units[i].classList.contains("show")){
            units[i].classList.remove("show")
            if (i === 0){
                units[units.length-1].classList.add("show");
                select.selectedIndex = units.length-1;
                break;
            }
            else {
                units[i - 1].classList.add("show");
                select.selectedIndex = i-1;
                break;
            }
        }
    }
}
function unitArrowDown(elmnt){
    let units = elmnt.parentNode.children[2].children;
    let length = units.length;
    let select = elmnt.parentNode.children[0];
    for (i=0; i<length; i++){
        if (units[i].classList.contains("show")){
            units[i].classList.remove("show")
            if (i === length-1){
                units[0].classList.add("show");
                select.selectedIndex = 0;
                break;
            }
            else {
                units[i + 1].classList.add("show");
                select.selectedIndex = i+1;
                break;
            }
        }
    }
}


let errorMessageContainers = document.getElementsByClassName("error-messages");
while ( errorMessageContainers.length !== 0 ){
    initiateAlertMessages(errorMessageContainers[0]);
}
function initiateAlertMessages(element) {
    let inputField = element.previousElementSibling;
    let errorSpans  = document.createElement("span");
    errorSpans.setAttribute("class", "alert-message");
    errorSpans.innerHTML = element.innerHTML;

    if ( element.children.length !== 0 ) {
        inputField.classList.add('alert');
        inputField.appendChild(errorSpans);
    }
    element.remove();
}