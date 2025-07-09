class Response {
  // This class represents the response from the handwriting analysis API.
  final String trait1; // Emotional Stability
  final String trait2; // Mental Energy
  final String trait3; // Modesty
  final String trait4; // Personal Harmony and flexibility
  final String trait5; // lack of dicipline
  final String trait6; // Poor Concentration
  final String trait7; // Non Communicativeness
  final String trait8; // Social Isolation

  Response({
    required this.trait1,
    required this.trait2,
    required this.trait3,
    required this.trait4,
    required this.trait5,
    required this.trait6,
    required this.trait7,
    required this.trait8,
  });
}

    //  "trait_1": "Stable" if trait_1 == 1 else "Not Stable",
    //         "trait_2": "High or Average" if trait_2 == 1 else "Low",
    //         "trait_3": "Observed" if trait_3 == 1 else "Not Observed",
    //         "trait_4": "Harmonious" if trait_4 == 1 else "Non Harmonious",
    //         "trait_5": "Observed" if trait_5 == 1 else "Not Observed",
    //         "trait_6": "Observed" if trait_6 == 1 else "Not Observed",
    //         "trait_7": "Observed" if trait_7 == 1 else "Not Observed",
    //         "trait_8": "Observed" if trait_8 == 1 else "Not Observed"