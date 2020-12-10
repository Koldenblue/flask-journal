$(document).ready(() => {
  const allEntriesBtn = $("#all-entries-btn");
  const newEntriesBtn = $("#new-entries-btn");
  const moodSelect = $("#mood-select");

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
        let container = document.getElementById(`container-${event.target.id}`);
        document.getElementsByClassName('all-entries-container')[0].removeChild(container);
      }).catch(err => console.error(err));
    })
  }

  updateBtns = document.getElementsByClassName('update-btn');
  for (let i = 0, j = updateBtns.length; i < j; i++) {
    updateBtns[i].addEventListener('click', (event) => {
      // the data-value corresponds to the id of the entry in the database. Send back with the query url to allow updating
      let queryUrl = '/update?id=' + event.target.dataset.value;
      // using an ajax 'get' will cause the template not to be rendered.
      // instead the html page is returned to this script
      window.location.href = queryUrl
    })
  }


  if (window.location.pathname === "/update") {
    console.log(moodSelect)
    console.log(moodSelect[0].dataset.value)
    console.log(moodSelect[0].selectedIndex)
    console.log(moodSelect[0].children[1].selected)
    console.log(moodSelect[0].children[1].innerText)
    let targetMood = moodSelect[0].dataset.value;
    for (let i = 0, j = moodSelect[0].children.length; i < j; i++) {
      if (moodSelect[0].children[i].innerText.toLowerCase() === targetMood) {
        moodSelect[0].children[i].selected = true;
      }
    }
  }
})