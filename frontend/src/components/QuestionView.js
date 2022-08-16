import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    fetch(`http://localhost:5000/questions?page=${this.state.page}`).then(resource => {
      return resource.json();
    }).then(result => {
      this.setState({
        questions: result.questions,
        totalQuestions: result.total_questions,
        categories: result.categories,
      });
    }).catch(error => {
      alert('Unable to load questions. Please try your request again');
    })
  };

  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id) => {

    fetch(`localhost:5000/category?category=${id}`).then(res => {
      return res.json();
    }).then(result => {
      this.setState({
        questions: result.questions,
        totalQuestions: result.total_questions,
        categories: result.categories,
        currentCategory: id,
      });
    }).catch(error => {
      alert('Unable to load categories. Please try your request again');
    })

  };

  submitSearch = (searchTerm) => {
    fetch(`localhost:5000/search?search=${searchTerm}`).then(res => {
      return res.json();
    }).then(result => {
      this.setState({
        questions: result.questions,
        totalQuestions: result.total_questions,
        categories: result.categories,
      });
    }).catch(error => {
      alert('Unable to load questions. Please try your request again');
    })
  };

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        fetch(`http://localhost:5000/questions/${id}`, {
          method: 'DELETE',
        }).then(res => {
          return res.json();
        }).then(result => {
          return result;
        }).catch(error => {
          alert('Unable to delete question. Please try your request again');
        })
      }
    }
  };

  render() {
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {Object.keys(this.state.categories).map((id) => (
              <li
                key={id}
                onClick={() => {
                  this.getByCategory(id);
                }}
              >
                {this.state.categories[id]}
                <img
                  className='category'
                  alt={`${this.state.categories[id].toLowerCase()}`}
                  src={`${this.state.categories[id].toLowerCase()}.svg`}
                />
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className='questions-list'>
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className='pagination-menu'>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
