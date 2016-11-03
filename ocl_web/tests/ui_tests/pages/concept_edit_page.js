var ConceptEditPage = function() {
    this.updateCommentTextArea = element(by.id("id_update_comment"));
    this.namesDiv= element(by.id("names-and-synonyms"));
    this.updateButton = element(by.id("update-concept"));
    this.cancelUpdateButton = element(by.id('cancel-update'));
    this.errorBox = element(by.css('.alert-error'));

    this.fillInUpdateText = function(updateMsg){
        this.updateCommentTextArea.sendKeys(updateMsg);
    }
};

module.exports = ConceptEditPage;
