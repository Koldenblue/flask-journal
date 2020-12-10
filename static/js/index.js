$(document).ready(() => {
  const allEntriesBtn = $("#all-entries-btn");
  const newEntriesBtn = $("#new-entries-btn");

  // make the menu buttons redirect properly
  allEntriesBtn.on('click', () => {
    window.location.href = '/allentries'
  })

  newEntriesBtn.on('click', () => {
    window.location.href = '/'
  })

  // add delete events to the delete buttons
  delBtns = document.getElementsByClassName('del-btn');
  console.log(delBtns)
  for (let i = 0, j = delBtns.length; i < j; i++) {
    delBtns[i].addEventListener('click', (event) => {
      // each button has an id corresponding to the entry in the SQL database
      console.log('clicked', event.target.id)
      let queryUrl = "/allentries" + "?id=" + event.target.id
      $.ajax({
        url: queryUrl,
        type: "DELETE"
      }).then((data) => {
        console.log(event.target.id)
        let container = document.getElementById(`container-${event.target.id}`)
        document.getElementsByClassName('all-entries-container')[0].removeChild(container)
      }).catch(err => console.error(err))
    })
  }
})