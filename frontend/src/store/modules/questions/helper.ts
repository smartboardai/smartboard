
export const initState = (): API.Discussion => ({
  id: '',
  title: '',
  content: '',
  category: 'general',
  createdAt: '',
  updatedAt: '',
  userId: '',
  files: []
})

export interface DiscussionState {
  discussions: API.Discussion[]
  currentDiscussion: API.Discussion | null
} 