---
created: 2026-01-02 11:59:46.490901
id: 01KDZ5T3NTY2XB0AA5W4DMMJXG
next_review: '2026-01-09'
prereqs: []
review_count: 1
source_id: 01KDZ5S2Y8EJZ7GGJVMF3SGP85
status: passed
timebox_min: 10
topics:
- LLM Prompting
- Content Generation
- Backend Development
- Metadata Optimization
type: drill
---

# Generate Enhanced Video Metadata with an LLM

## Pattern
- Provide an LLM with raw or minimal content metadata (e.g., video title).
- Instruct the LLM to generate enriched metadata (e.g., detailed descriptions, relevant tags, improved titles).
- Ensure the generated content is contextually relevant and includes elements like hashtags.
- Aim for 'oneshot capability' where the LLM produces high-quality output on the first try.

## Drill
**Goal:** Use an AI model to automatically enhance a video's description and generate relevant tags based on its title and context.

**Steps:**
1. Choose a short video or a video idea with a simple title (e.g., 'Vibe Coding No Talking Stream' as used at 07:32).
2. Identify the current (or hypothetical) minimal description and lack of tags.
3. Craft a prompt for a capable LLM (like Gemini 3 Pro) asking it to enhance the video's description and suggest a list of relevant tags.
4. Specify that the description should be more engaging, include hashtags, and provide more context about the video (as demonstrated at 08:03).
5. Review the generated description and tags for relevance, quality, and inclusion of requested elements.

## Snippet
```prompt
I need to enhance the metadata for a YouTube video. The current title is 'Vibe Coding No Talking Stream #6'. It currently has no description and no tags.

Please generate:
1.  An improved, engaging description for this video. It should provide more context about what 'vibe coding' is, what viewers can expect (e.g., focus, atmosphere), and include relevant hashtags (as shown at 08:06).
2.  A list of 10-15 highly relevant tags for this video to improve its discoverability (as shown at 08:15).

Assume the video is a live coding session focused on productivity and a relaxed atmosphere, without commentary.
```

## Validation
- [ ] The generated description is significantly longer and more detailed than the original.
- [ ] The description includes relevant hashtags.
- [ ] The generated tags are highly relevant to the video's content and context.
- [ ] The output demonstrates a good understanding of the video's context from minimal input.
- [ ] The enhancement was achieved in a single prompt ('oneshot capability' mentioned at 08:26).

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
