$('input[type=radio]').change(function() {
    $('.sort-choice').removeClass('checked');
    $(this).parent().addClass('checked');
});

$('.sort span.sort-label').click(function() {
    $('.sort span.sort-label').removeClass('checked');
    $(this).addClass('checked');
});

// Editing the simulation name
$('button.action.edit').click(function(e) {

    // In order to have each item work as a link we need to stopPropagation on all children elements that have click events
    e.stopPropagation();

    let editBtn = this;
    let tableItem = editBtn.parentNode.parentNode;
    let textContainer = tableItem.children[1].children[0];
    let editActions = tableItem.children[1].children[1];

    if ( textContainer.contentEditable === "false" ){

        let text = textContainer.innerHTML;

        textContainer.addEventListener('keydown', (evt) => {
            if(evt.keyCode == 13)
                editActions.children[1].click();
            if(evt.keyCode == 27)
                editActions.children[0].click();
        });

        if ( textContainer.contentEditable === "false" ){

            textContainer.contentEditable = "true";

            if (editActions.classList.contains('hidden'))
                editActions.classList.remove('hidden')

        }

        editActions.children[0].addEventListener('click', function (e) {

            // In order to have each item work as a link we need to stopPropagation on all children elements that have click events
            e.stopPropagation();

            console.log('discard');

            textContainer.innerHTML=text;

            textContainer.contentEditable = false;

            if (!editActions.classList.contains('hidden'))
                editActions.classList.add('hidden')

            remakeChildren(editActions);

        });

        editActions.children[1].addEventListener('click', function (e) {

            // In order to have each item work as a link we need to stopPropagation on all children elements that have click events
            e.stopPropagation();

            console.log('save');

            textContainer.contentEditable = false;

            $(textContainer).text(function(index, currentText) {
                return currentText.substr(0, 80);
            });

            text = textContainer.innerHTML;

            if (!editActions.classList.contains('hidden'))
                editActions.classList.add('hidden')

            remakeChildren(editActions);

        });

    }

});
function remakeChildren(parent){

    let oldchild1 = parent.children[0];
    let newchild1 = oldchild1.cloneNode(true);
    let oldchild2 = parent.children[1];
    let newchild2 = oldchild2.cloneNode(true);

    parent.replaceChild(newchild1, oldchild1);
    parent.replaceChild(newchild2, oldchild2);

    console.log('replaced');
}

// In order to have each item work as a link we need to stopPropagation on all children elements that have click events
$('div.structured.name').click(function(e) {
    if (this.firstElementChild.contentEditable === "true" )
        e.stopPropagation();
});

// Makes the item to act like a link
$('div.simulations-table-item').click(function (e){

    // Checks to make sure it was directly clicked
    // So there are to two layers to ensure that the item was clicked directly (target and stopPropagation)
    if (e.target === this || e.target === this.children[0] || e.target === this.children[2] || e.target === this.children[3]) {
        //clicks the form containing the link to the url
        this.children[5].children[0].click();
    }
    if (e.target === this.children[1] || e.target === this.children[1].children[0]){
        if(this.children[1].children[0].contentEditable !== "true"){
            this.children[5].children[0].click();
        }
    }
    if (e.target === this.children[0].children[0] || e.target === this.children[0].children[0].children[0] ){
            this.children[5].children[0].click();
    }
});

// Shows the delete modal and fills the data
$('button.action.remove').click(function(e) {

    // In order to have each item work as a link we need to stopPropagation on all children elements that have click events
    e.stopPropagation();

    let modalBack = document.getElementsByClassName('delete-modal-overlay-back')[0];
    if (!modalBack.classList.contains('show'))
        modalBack.classList.add('show')

    let modalBody = modalBack.children[0]

    let removeBtn = this;
    let tableItem = removeBtn.parentNode.parentNode;
    let name = tableItem.children[1].children[0].innerHTML;
    let deleteUrl = tableItem.children[6].innerHTML;

    modalBody.children[1].children[0].children[0].children[0].innerHTML = name;
    modalBody.children[2].action=deleteUrl;
});

// delete modal interactions
$('.delete-modal-overlay-back').on('click', function(e) {
    if (e.target !== this)
        return;
    $('.delete-modal-overlay-back').toggleClass('show');
});
$('.delete-modal-overlay-back button').on('click', function(e) {
    if (e.target !== this)
        return;
    $('.delete-modal-overlay-back').toggleClass('show');
});

