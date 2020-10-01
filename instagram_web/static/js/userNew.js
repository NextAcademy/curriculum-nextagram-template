console.log('shoot')

$(document).ready(() => {
    passInput = $('#passInput')
    passInput.keyup(() => {
        if (passInput.val().length < 7) {
            $('#passReply').text('That is too short, boi')
        }
        else {
            $('#passReply').text('That is a gucci length')
        }
    })
})
