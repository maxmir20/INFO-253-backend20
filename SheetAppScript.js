function getFormChoices(url, mealTitle){  
    var form = FormApp.openByUrl(url);
    var qs = form.getItems(FormApp.ItemType.CHECKBOX);
    
    var formChoices = {};
    for (var item in qs){
      //Logger.log(qs[item].getTitle());
      //Logger.log(mealTitle);
  
      if (qs[item].getTitle() == mealTitle){
        
        var cb_item = qs[item].asCheckboxItem();
        var options = cb_item.getChoices();
        //Logger.log(options);
        for (var choice in options){
          formChoices[options[choice].getValue()] = false;
        }   
      }
    }
    return formChoices;
  }
  
  
  
  function convertCellsToDictionary(){
    var sheet = SpreadsheetApp.getActiveSheet();
    var formUrl = sheet.getFormUrl();
    
    
    // Iterate through headers to find lunch or dinner
    
    var sheetLength = sheet.getLastColumn();
    
    var lastRow = sheet.getLastRow();
    var mealColumn = null;
    
    for (let column = 1; column <= sheetLength; column++) {
      //search header for meals
      var currentHeaderCell = sheet.getRange(1,column);
      var currentTitle = currentHeaderCell.getValue();
      Logger.log(currentTitle);
      if (currentTitle.includes("Lunch") || currentTitle.includes("Dinner")){
        // If found, save header title and column index
        
        // Go to last row, capture userchoices in csv format using column index and convert to array
        var userChoiceCell = sheet.getRange(lastRow, column);
        var userChoiceString = userChoiceCell.getValue();
        var userChoiceArray = userChoiceString.split(',');
  
        // get formChoices by matching header title, return formChoices dictionary
        var formChoices = getFormChoices(formUrl, currentTitle);
        
        // update formchoices with userchoices
        Logger.log(formChoices);
        Logger.log(userChoiceArray);
        for (var userChoice in userChoiceArray){
          trimChoice = userChoiceArray[userChoice].trim();
          if (trimChoice in formChoices) {
            formChoices[trimChoice] = true;
          }
        }
          // replace cell with dictionary values 
        if (!isEmpty(formChoices) && userChoiceArray[0].length > 0){
          userChoiceCell.setValue(formChoices);
        }
      }
    } 
  }
  
  
  function isEmpty(obj) {
      for(var key in obj) {
          if(obj.hasOwnProperty(key))
              return false;
      }
      return true;
  }