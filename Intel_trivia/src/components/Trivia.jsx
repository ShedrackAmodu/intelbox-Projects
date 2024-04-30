import {
  Container,
  Text,
  Flex,
  Heading,
  Button,
  CircularProgress,
  CircularProgressLabel,
  VStack,
} from "@chakra-ui/react";
import PropTypes from "prop-types";
import { EntertainmentQuestions } from "../data/categories/entertainment";
import { HistoryQuestions } from "../data/categories/history";
import { MathQuestions } from "../data/categories/maths";
import { ProgrammingQuestions } from "../data/categories/programming";
import { ScienceQuestions } from "../data/categories/science";
import { useState, useEffect } from "react";

const Trivia = ({ prop }) => {
  const [questions, setQuestions] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [totalQuestionAnswered, setTotalQuestionAnswered] = useState(0);
  const [totalCorrectAnswers, setTotalCorrectAnswers] = useState(0);
  const [totalWrongAnswers, setTotalWrongAnswers] = useState(0);
  let [timeLeft, setTimeLeft] = useState(prop === "math" ? 30 : 10);

  useEffect(() => {
    // Function to set questions based on the prop value
    const setQuestionsBasedOnProp = () => {
      switch (prop) {
        case "entertainment":
          setQuestions(EntertainmentQuestions);
          break;
        case "history":
          setQuestions(HistoryQuestions);
          break;
        case "math":
          setQuestions(MathQuestions);
          break;
        case "programming":
          setQuestions(ProgrammingQuestions);
          break;
        case "science":
          setQuestions(ScienceQuestions);
          break;
        default:
          setQuestions(null);
      }

      if (questions) {
        setQuestions(shuffleArray(questions));
      }
    };

    // a function that shuffles the questions
    function shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    }

    // Call the function to set questions when the component mounts or when the prop value changes
    setQuestionsBasedOnProp();
  }, [prop, questions]); // Run the effect whenever the prop value changes

  // handle options
  const handleOptions = (index) => {
    const clickedOption = questions[currentQuestionIndex].options[index];
    const correctAnswer = questions[currentQuestionIndex].correctAnswer;

    // Update background color of options based on correctness
    const options = document.querySelectorAll(".option");
    options.forEach((option, i) => {
      if (i === index) {
        if (clickedOption === correctAnswer) {
          option.style.backgroundColor = "green"; // Set background color to green for correct answer
          setTotalCorrectAnswers(totalCorrectAnswers + 1);
        } else {
          option.style.backgroundColor = "red"; // Set background color to red for clicked option (wrong answer)
          setTotalWrongAnswers(totalWrongAnswers + 1);
        }
      }
    });

    // Delay transition to next question
    setTimeout(() => {
      // Reset background colors
      options.forEach((option) => {
        option.style.backgroundColor = ""; // Reset background color to default
      });
      setTotalQuestionAnswered(totalQuestionAnswered + 1);
      setTimeLeft(prop === "math" ? 30 : 10);

      // Move to next question index
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }, 1000); // Delay for 1 second
  };

  // Countdown timer logic
  useEffect(() => {
    // Set the timeout duration based on the category
    const timeoutDuration = prop === "math" ? 30 : 10;

    if (timeLeft === 0) {
      // Move to the next question if time runs out+
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setTimeLeft(timeoutDuration); // Reset the countdown timer
    } else {
      // Update the countdown timer every second
      const timer = setTimeout(() => {
        setTimeLeft(timeLeft - 1);
      }, 1000);
      // Clean up the timer when the component unmounts or when the question changes
      return () => clearTimeout(timer);
    }
  }, [timeLeft, currentQuestionIndex, prop]); // Add currentQuestionIndex as a dependency

  // Render the current question and options, or a congratulatory message if at the end of the game
  return (
    <Container>
      {questions && questions.length > 0 && currentQuestionIndex < 20 ? (
        <>
          <Heading>{prop.toUpperCase()}</Heading>

          <CircularProgress
            value={timeLeft}
            max={prop === "math" ? 30 : 10}
            color="red"
            my="30px"
          >
            <CircularProgressLabel>{timeLeft}</CircularProgressLabel>
          </CircularProgress>
          <Text>{questions[currentQuestionIndex].question}</Text>
          <Flex
            gap="5"
            justify="center"
            align="center"
            flexWrap="wrap"
            width="100%"
            my="30px"
          >
            {questions[currentQuestionIndex].options.map((item, index) => (
              <Text
                key={index}
                className="option"
                onClick={() => handleOptions(index)}
                w="40%"
              >
                {item}
              </Text>
            ))}
          </Flex>
          <Button
            onClick={() => {
              setCurrentQuestionIndex(currentQuestionIndex + 1);
              setTimeLeft(prop === "math" ? 30 : 10);
            }}
          >
            Skip
          </Button>
        </>
      ) : (
        <VStack gap="20px" justify="center" align="center">
          <Heading>
            Congratulations! You have reached the end of the trivia.
          </Heading>
          <Text>Total Trivia Questions: 20</Text>
          <Text>Total Questions Answered: {totalQuestionAnswered}</Text>
          <Text>Total Correct Answers: {totalCorrectAnswers}</Text>
          <Text>Total Wrong Answers: {totalWrongAnswers}</Text>
          <Button onClick={() => window.location.reload()}>
            Start a new game
          </Button>
        </VStack>
      )}
    </Container>
  );
};

Trivia.propTypes = {
  prop: PropTypes.string.isRequired,
};

export default Trivia;
