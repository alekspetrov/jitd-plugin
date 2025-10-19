/**
 * User Routes - POST endpoint example with validation
 *
 * @route POST /api/users
 * @access Private
 */

import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { authMiddleware } from '../middleware/auth';
import { validateRequest } from '../middleware/validation';

const router = Router();

// Validation schema
const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(18).optional(),
});

type CreateUserInput = z.infer<typeof createUserSchema>;

/**
 * POST /api/users
 * @description Create new user
 * @access Private
 */
router.post(
  '/api/users',
  authMiddleware,
  validateRequest(createUserSchema),
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userData: CreateUserInput = req.body;

      // TODO: Save user to database
      const newUser = await createUser(userData);

      res.status(201).json({
        success: true,
        data: newUser,
      });
    } catch (error) {
      next(error);
    }
  }
);

export default router;

// Mock function (replace with actual database insert)
async function createUser(data: CreateUserInput) {
  return {
    id: '123',
    ...data,
    createdAt: new Date(),
  };
}
