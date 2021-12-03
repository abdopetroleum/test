$('input[type=radio]').change(function() {
    $('.sort-choice').removeClass('checked');
    $(this).parent().addClass('checked');
});

$('.sort span.sort-label').click(function() {
    $('.sort span.sort-label').removeClass('checked');
    $(this).addClass('checked');
});

$('button.action.edit').on('click', function () {

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

        editActions.children[0].addEventListener('click', function () {

            console.log('discard');

            textContainer.innerHTML=text;

            textContainer.contentEditable = false;

            if (!editActions.classList.contains('hidden'))
                editActions.classList.add('hidden')

            remakeChildren(editActions);

        });

        editActions.children[1].addEventListener('click', function () {

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

    console.log('replaced')
}
