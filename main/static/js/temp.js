// this is a temporary script to show and hide charts

function chartsToggle(target) {

    if (!target.classList.contains('active'))
        target.classList.add('active')
    else
        target.classList.remove('active')

    $('.sub-grid').toggleClass('hidden');

}