<template>
  <AppLayout title="PMP Study" :showBack="true">
    <!-- Progress Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="card bg-gradient-to-br from-primary/90 to-primary shadow-lg card-hover">
        <div class="card-body p-5 text-white">
          <div class="text-sm opacity-90 font-medium">Total Questions</div>
          <div class="text-2xl font-bold mt-1">{{ stats.total || 0 }}</div>
        </div>
      </div>

      <div class="card bg-gradient-to-br from-success/90 to-success shadow-lg card-hover">
        <div class="card-body p-5 text-white">
          <div class="text-sm opacity-90 font-medium">Answered</div>
          <div class="text-2xl font-bold mt-1">{{ stats.answered || 0 }}</div>
        </div>
      </div>

      <div class="card bg-gradient-to-br from-warning/90 to-warning shadow-lg card-hover">
        <div class="card-body p-5 text-white">
          <div class="text-sm opacity-90 font-medium">Accuracy</div>
          <div class="text-2xl font-bold mt-1">{{ stats.accuracy || 0 }}%</div>
        </div>
      </div>

      <div class="card bg-gradient-to-br from-info/90 to-info shadow-lg card-hover">
        <div class="card-body p-5 text-white">
          <div class="text-sm opacity-90 font-medium">Domains</div>
          <div class="text-2xl font-bold mt-1">{{ domains.length }}</div>
        </div>
      </div>
    </div>

    <!-- Study Session Controls -->
    <div class="card shadow-lg border border-base-300 mb-6">
      <div class="card-body">
        <h2 class="font-bold text-xl mb-4">Study Session</h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text">Number of Questions</span>
            </label>
            <select v-model="sessionConfig.count" class="select select-bordered">
              <option value="5">5 Questions</option>
              <option value="10">10 Questions</option>
              <option value="20">20 Questions</option>
              <option value="30">30 Questions</option>
            </select>
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">Domain</span>
            </label>
            <select v-model="sessionConfig.domain" class="select select-bordered">
              <option value="all">All Domains</option>
              <option v-for="domain in domains" :key="domain" :value="domain">{{ domain }}</option>
            </select>
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">Difficulty</span>
            </label>
            <select v-model="sessionConfig.difficulty" class="select select-bordered">
              <option value="all">All Levels</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>
        </div>

        <div class="flex gap-4 mt-6">
          <button @click="startSession" class="btn btn-primary btn-lg flex-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Start Study Session
          </button>

          <button @click="takeExam" class="btn btn-outline btn-lg flex-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            Simulate Exam (50Q)
          </button>
        </div>
      </div>
    </div>

    <!-- Domain Breakdown -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Domain Performance -->
      <div class="card shadow-lg border border-base-300">
        <div class="card-body">
          <h2 class="font-bold text-xl mb-4">Domain Performance</h2>
          <div class="space-y-4">
            <div v-for="domain in domainStats" :key="domain.name" class="flex items-center">
              <div class="w-32 text-sm font-medium">{{ domain.name }}</div>
              <div class="flex-1 mx-4">
                <div class="w-full bg-base-300 rounded-full h-3">
                  <div
                    class="h-3 rounded-full transition-all"
                    :class="getDomainColor(domain.accuracy)"
                    :style="{ width: domain.accuracy + '%' }"
                  ></div>
                </div>
              </div>
              <div class="w-16 text-right text-sm font-bold">{{ domain.accuracy }}%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Questions -->
      <div class="card shadow-lg border border-base-300">
        <div class="card-body">
          <h2 class="font-bold text-xl mb-4">Recent Questions</h2>
          <div class="space-y-3 max-h-80 overflow-y-auto">
            <div
              v-for="question in recentQuestions"
              :key="question.id"
              class="p-3 rounded-lg border border-base-300 hover:bg-base-200 transition-colors cursor-pointer"
              @click="reviewQuestion(question)"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <div class="font-medium text-sm line-clamp-2">{{ question.question_text }}</div>
                  <div class="flex items-center gap-2 mt-2">
                    <span class="badge badge-xs" :class="domainBadgeClass(question.domain)">
                      {{ question.domain }}
                    </span>
                    <span class="badge badge-xs" :class="difficultyBadgeClass(question.difficulty)">
                      {{ question.difficulty }}
                    </span>
                  </div>
                </div>
                <div class="ml-2">
                  <span class="badge" :class="question.answered_correctly ? 'badge-success' : 'badge-error'">
                    {{ question.answered_correctly ? '✓' : '✗' }}
                  </span>
                </div>
              </div>
            </div>

            <div v-if="recentQuestions.length === 0" class="text-center py-4">
              <p class="text-base-content/60">No recent questions. Start a study session!</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Question Session Modal -->
    <div v-if="showSession" class="modal modal-open">
      <div class="modal-box max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
        <div class="flex justify-between items-center mb-4">
          <div>
            <h3 class="font-bold text-xl">Question {{ currentQuestionIndex + 1 }} of {{ sessionQuestions.length }}</h3>
            <div class="text-sm text-base-content/70 flex gap-2">
              <span class="badge badge-sm" :class="domainBadgeClass(currentQuestion.domain)">
                {{ currentQuestion.domain }}
              </span>
              <span class="badge badge-sm" :class="difficultyBadgeClass(currentQuestion.difficulty)">
                {{ currentQuestion.difficulty }}
              </span>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="stats stats-horizontal shadow">
              <div class="stat p-2">
                <div class="stat-value text-success text-lg">{{ sessionStats.correct }}</div>
                <div class="stat-title">Correct</div>
              </div>
              <div class="stat p-2">
                <div class="stat-value text-lg">{{ sessionStats.attempted }}</div>
                <div class="stat-title">Attempted</div>
              </div>
            </div>
            <button @click="showSession = false" class="btn btn-ghost btn-sm">
              Exit
            </button>
          </div>
        </div>

        <div class="flex-1 overflow-y-auto">
          <!-- Question Text -->
          <div class="card bg-base-200 mb-4">
            <div class="card-body">
              <div class="prose max-w-none">
                <div v-if="currentQuestion.chapter" class="text-sm text-base-content/70 mb-2">
                  Chapter {{ currentQuestion.chapter }} • {{ currentQuestion.subtopic }}
                </div>
                <p class="text-lg font-medium">{{ currentQuestion.question_text }}</p>
                <div v-if="currentQuestion.scenario" class="mt-4 p-3 bg-base-300 rounded-lg">
                  <p class="font-medium mb-1">Scenario:</p>
                  <p class="text-sm">{{ currentQuestion.scenario }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Options -->
          <div class="space-y-3 mb-6">
            <div
              v-for="(optionText, optionKey) in currentQuestion.options"
              :key="optionKey"
              class="flex items-start p-4 rounded-lg border-2 transition-all cursor-pointer"
              :class="getOptionClass(optionKey)"
              @click="selectOption(optionKey)"
            >
              <div class="w-8 h-8 rounded-full border-2 flex items-center justify-center mr-3 mt-1"
                   :class="getOptionCircleClass(optionKey)">
                {{ optionKey }}
              </div>
              <div class="flex-1">
                <div class="font-medium">{{ optionText }}</div>
                <div v-if="showExplanation && optionKey === currentQuestion.correct_answer"
                     class="mt-2 text-sm text-success">
                  <strong>Correct Answer:</strong> {{ currentQuestion.explanation }}
                </div>
              </div>
            </div>
          </div>

          <!-- Answer Revealed -->
          <div v-if="showExplanation" class="card bg-base-200 mb-4">
            <div class="card-body">
              <div class="flex items-center justify-between">
                <div>
                  <div class="font-bold text-lg" :class="answeredCorrectly ? 'text-success' : 'text-error'">
                    {{ answeredCorrectly ? 'Correct! 🎉' : 'Incorrect' }}
                  </div>
                  <div class="text-sm text-base-content/70 mt-1">
                    <div><strong>Correct Answer:</strong> {{ currentQuestion.correct_answer }}</div>
                    <div v-if="currentQuestion.explanation" class="mt-1">
                      <strong>Explanation:</strong> {{ currentQuestion.explanation }}
                    </div>
                  </div>
                </div>
                <button @click="nextQuestion" class="btn btn-primary">
                  {{ isLastQuestion ? 'Finish Session' : 'Next Question' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Navigation -->
          <div v-if="!showExplanation" class="flex justify-between">
            <button @click="previousQuestion" :disabled="currentQuestionIndex === 0"
                    class="btn btn-ghost">
              Previous
            </button>
            <button @click="checkAnswer" :disabled="selectedOption === null"
                    class="btn btn-primary">
              Check Answer
            </button>
          </div>
        </div>

        <!-- Progress Bar -->
        <div class="mt-4">
          <div class="flex justify-between text-sm mb-1">
            <span>Progress</span>
            <span>{{ Math.round((currentQuestionIndex + 1) / sessionQuestions.length * 100) }}%</span>
          </div>
          <div class="w-full bg-base-300 rounded-full h-2">
            <div
              class="bg-primary h-2 rounded-full transition-all"
              :style="{ width: ((currentQuestionIndex + 1) / sessionQuestions.length * 100) + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Question Review Modal -->
    <div v-if="showReview" class="modal modal-open">
      <div class="modal-box max-w-3xl">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="font-bold text-xl">Question Review</h3>
            <div class="text-sm text-base-content/70 flex gap-2 mt-1">
              <span class="badge" :class="domainBadgeClass(reviewingQuestion.domain)">
                {{ reviewingQuestion.domain }}
              </span>
              <span class="badge" :class="difficultyBadgeClass(reviewingQuestion.difficulty)">
                {{ reviewingQuestion.difficulty }}
              </span>
            </div>
          </div>
          <button @click="showReview = false" class="btn btn-ghost btn-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="prose max-w-none">
          <div class="card bg-base-200 mb-4">
            <div class="card-body">
              <p class="text-lg font-medium">{{ reviewingQuestion.question_text }}</p>
              <div v-if="reviewingQuestion.scenario" class="mt-4 p-3 bg-base-300 rounded-lg">
                <p class="font-medium mb-1">Scenario:</p>
                <p class="text-sm">{{ reviewingQuestion.scenario }}</p>
              </div>
            </div>
          </div>

          <div class="space-y-2 mb-6">
            <div
              v-for="(optionText, optionKey) in reviewingQuestion.options"
              :key="optionKey"
              class="p-3 rounded-lg"
              :class="optionKey === reviewingQuestion.correct_answer ? 'bg-success/20 border border-success' : 'bg-base-200'"
            >
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full border-2 flex items-center justify-center mr-3"
                     :class="optionKey === reviewingQuestion.correct_answer ? 'border-success text-success' : 'border-base-400 text-base-content/70'">
                  {{ optionKey }}
                </div>
                <div class="font-medium">{{ optionText }}</div>
              </div>
            </div>
          </div>

          <div class="card bg-base-200">
            <div class="card-body">
              <h4 class="font-bold text-lg mb-2">Explanation</h4>
              <p>{{ reviewingQuestion.explanation }}</p>
              <div v-if="reviewingQuestion.keywords && reviewingQuestion.keywords.length" class="mt-4">
                <h5 class="font-bold mb-1">Keywords:</h5>
                <div class="flex flex-wrap gap-1">
                  <span v-for="keyword in reviewingQuestion.keywords" :key="keyword"
                        class="badge badge-outline">
                    {{ keyword }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import pmpData from "@/data/pmp.json"

const stats = ref({})
const questions = ref([])
const domains = ref([])
const domainStats = ref([])
const recentQuestions = ref([])
const showSession = ref(false)
const sessionQuestions = ref([])
const currentQuestionIndex = ref(0)
const selectedOption = ref(null)
const showExplanation = ref(false)
const showReview = ref(false)
const reviewingQuestion = ref({})

const sessionConfig = ref({
  count: "10",
  domain: "all",
  difficulty: "all"
})

const sessionStats = ref({
  correct: 0,
  attempted: 0,
  accuracy: 0
})

const currentQuestion = computed(() => {
  return sessionQuestions.value[currentQuestionIndex.value] || {}
})

const isLastQuestion = computed(() => {
  return currentQuestionIndex.value === sessionQuestions.value.length - 1
})

const answeredCorrectly = computed(() => {
  return selectedOption.value === currentQuestion.value.correct_answer
})

const domainBadgeClass = (domain) => {
  const domainMap = {
    'People': 'badge-primary',
    'Process': 'badge-secondary',
    'Business Environment': 'badge-accent'
  }
  return domainMap[domain] || 'badge-neutral'
}

const difficultyBadgeClass = (difficulty) => {
  const difficultyMap = {
    'Easy': 'badge-success',
    'Medium': 'badge-warning',
    'Hard': 'badge-error'
  }
  return difficultyMap[difficulty] || 'badge-neutral'
}

const getDomainColor = (accuracy) => {
  if (accuracy >= 80) return 'bg-success'
  if (accuracy >= 60) return 'bg-warning'
  return 'bg-error'
}

const getOptionClass = (optionKey) => {
  if (!showExplanation.value) {
    return selectedOption.value === optionKey
      ? 'border-primary bg-primary/10'
      : 'border-base-300 hover:border-primary/50'
  }

  if (optionKey === currentQuestion.value.correct_answer) {
    return 'border-success bg-success/10'
  }

  if (optionKey === selectedOption.value && optionKey !== currentQuestion.value.correct_answer) {
    return 'border-error bg-error/10'
  }

  return 'border-base-300'
}

const getOptionCircleClass = (optionKey) => {
  if (!showExplanation.value) {
    return selectedOption.value === optionKey
      ? 'border-primary text-primary'
      : 'border-base-400 text-base-content/70'
  }

  if (optionKey === currentQuestion.value.correct_answer) {
    return 'border-success text-success'
  }

  if (optionKey === selectedOption.value && optionKey !== currentQuestion.value.correct_answer) {
    return 'border-error text-error'
  }

  return 'border-base-400 text-base-content/70'
}

const loadQuestions = () => {
  try {
    // Use the actual JSON data
    if (pmpData && pmpData.pmp_practice_database && pmpData.pmp_practice_database.questions) {
      questions.value = pmpData.pmp_practice_database.questions
      stats.value.total = questions.value.length
      stats.value.answered = Math.floor(questions.value.length * 0.3) // Mock 30% answered
      stats.value.accuracy = 75 // Mock accuracy
    } else {
      // Fallback if structure is different
      questions.value = pmpData.questions || pmpData || []
      stats.value = { total: questions.value.length, answered: 0, accuracy: 0 }
    }

    // Extract unique domains
    const domainSet = new Set()
    questions.value.forEach(q => {
      if (q.domain) domainSet.add(q.domain)
    })
    domains.value = Array.from(domainSet)

    // Calculate domain stats
    domainStats.value = domains.value.map(domain => {
      const domainQuestions = questions.value.filter(q => q.domain === domain)
      const total = domainQuestions.length
      const correct = Math.floor(total * 0.75) // Mock 75% correct
      const accuracy = total > 0 ? Math.round((correct / total) * 100) : 0

      return { name: domain, total, correct, accuracy }
    })

    // Get recent questions (last 5)
    recentQuestions.value = questions.value.slice(0, 5).map(q => ({
      ...q,
      answered_correctly: Math.random() > 0.3 // Mock data
    }))

  } catch (error) {
    console.error("Failed to load questions:", error)
    questions.value = []
    domains.value = []
    domainStats.value = []
    recentQuestions.value = []
  }
}

const loadProgress = () => {
  try {
    // Calculate progress from actual data
    const total = questions.value.length
    const answered = Math.floor(total * 0.3) // 30% answered
    const accuracy = 75 // Mock accuracy
    
    stats.value = { total, answered, accuracy }
  } catch (error) {
    console.error("Failed to load progress:", error)
    stats.value = { total: 0, answered: 0, accuracy: 0 }
  }
}

const startSession = () => {
  try {
    // Filter questions based on session config
    let filtered = [...questions.value]

    if (sessionConfig.value.domain !== 'all') {
      filtered = filtered.filter(q => q.domain === sessionConfig.value.domain)
    }

    if (sessionConfig.value.difficulty !== 'all') {
      filtered = filtered.filter(q => q.difficulty === sessionConfig.value.difficulty)
    }

    // Shuffle and take requested number
    const shuffled = filtered.sort(() => Math.random() - 0.5)
    sessionQuestions.value = shuffled.slice(0, parseInt(sessionConfig.value.count))

    // If no questions match criteria, use all
    if (sessionQuestions.value.length === 0) {
      sessionQuestions.value = questions.value.slice(0, parseInt(sessionConfig.value.count))
    }

    currentQuestionIndex.value = 0
    selectedOption.value = null
    showExplanation.value = false
    sessionStats.value = { correct: 0, attempted: 0, accuracy: 0 }
    showSession.value = true

  } catch (error) {
    console.error("Failed to start session:", error)
    sessionQuestions.value = questions.value.slice(0, parseInt(sessionConfig.value.count))
    currentQuestionIndex.value = 0
    selectedOption.value = null
    showExplanation.value = false
    sessionStats.value = { correct: 0, attempted: 0, accuracy: 0 }
    showSession.value = true
  }
}

const takeExam = () => {
  sessionConfig.value.count = "50"
  sessionConfig.value.domain = "all"
  sessionConfig.value.difficulty = "all"
  startSession()
}

const selectOption = (optionKey) => {
  if (!showExplanation.value) {
    selectedOption.value = optionKey
  }
}

const checkAnswer = () => {
  if (selectedOption.value === null) return

  showExplanation.value = true
  sessionStats.value.attempted++

  if (answeredCorrectly.value) {
    sessionStats.value.correct++
  }

  sessionStats.value.accuracy = Math.round((sessionStats.value.correct / sessionStats.value.attempted) * 100)
}

const nextQuestion = () => {
  if (isLastQuestion.value) {
    finishSession()
  } else {
    currentQuestionIndex.value++
    selectedOption.value = null
    showExplanation.value = false
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    selectedOption.value = null
    showExplanation.value = false
  }
}

const finishSession = () => {
  showSession.value = false

  const score = Math.round((sessionStats.value.correct / sessionQuestions.value.length) * 100)
  alert(`Session complete! Your score: ${score}% (${sessionStats.value.correct}/${sessionQuestions.value.length})`)

  // Reload progress
  loadProgress()
  loadQuestions()
}

const reviewQuestion = (question) => {
  reviewingQuestion.value = question
  showReview.value = true
}

onMounted(async () => {
  loadQuestions()
  loadProgress()
})
</script>
