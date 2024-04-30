import { Text, Container, Heading } from "@chakra-ui/react";

const Intro = () => {
  return (
    <Container >
      <Heading mb="20px">Welcome to IntelBox Trivia</Heading>
      <Text>
        Welcome to our trivia adventure, where you will stretch your mind across
        various topics. With brain-teasers spanning history, science,
        entertainment, programming and literature, join us on a journey of
        discovery and fun to elevate your IQ! Anwser all 20 questions and aim for a high score!
      </Text>
    </Container>
  );
};

export default Intro;
