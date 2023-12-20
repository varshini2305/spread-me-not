/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// Select the database to use.
use('facts');

// Insert a few documents into the sales collection.
db.fact_check_lines_explode.aggregate([
    {
      $search: {
        index: "article_search",
        text: {
          query: "beheaded babies israel",
          path: "processed_article",
          tokenize: "whitespace" // Specify the tokenization method
        },
        highlight: {
          path: "processed_article",
          meta: true
        }
      }
    },
    {
      $project: {
        _id: 0,
        hitRate: { $meta: "searchScore" },
        hitMatch: { $meta: "searchHighlights.processed_article" }
      }
    }
  ])
  